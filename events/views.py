from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import Prefetch
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from registration.models import UserProfile

from .models import Event, EventType, TeamRegistration
from .serializers import AllEventsSerializer, EventTypeSerializer

User = get_user_model()

# class EventView(ListAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = EventSerializer
#     model = Event
#     queryset = Event.objects.filter(published=True)
#     lookup_field = 'slug'


class AllEventsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AllEventsSerializer
    model = EventType
    queryset = EventType.objects.prefetch_related(
        Prefetch('events', queryset=Event.objects.filter(published=True), to_attr='published_events')
    )


class EventTypeView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EventTypeSerializer
    model = EventType

    def get(self, request, reference_name):
        eventType = EventType.objects.get(reference_name=reference_name)
        serializer = EventTypeSerializer(eventType)
        data = serializer.data

        if type(request.user) != AnonymousUser:
            user = User.objects.get(id=request.user.id)
            userprofile = UserProfile.objects.get(user=user)
            team = None

            for event in eventType.events.all():
                if event in userprofile.events_registered.all():
                    if event.team_event:
                        teams = TeamRegistration.objects.filter(event=event)

                        team = [t for t in teams if userprofile in t.members.all() or t.leader == userprofile][0]

                        d = {
                            "team": {
                                "id": team.id,
                                "name": team.name,
                                "leader": {
                                    "id": team.leader.registration_code,
                                    "name": team.leader.user.get_full_name()
                                },
                                "members": team.member_list()
                            }
                        }

                        for e in data["events"]:
                            if e["name"] == event.name:
                                e["is_registered"] = True
                                e["team"] = d["team"]
                            else:
                                e["is_registered"] = False

            if eventType.type == '4':
                data["antarang"] = team.leader.antarang
                data["aayam"] = team.leader.aayam
                data["nrityansh"] = team.leader.nrityansh
                data["cob"] = team.leader.cob

            return Response(data=data, status=status.HTTP_200_OK)

        return Response(serializer.data)


class RegisterEventAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        userprofile = UserProfile.objects.get(user=user)

        data = request.data
        event_name = data.get('event_name', None)

        event = Event.objects.get(name=event_name)

        userprofile.events_registered.add(event)

        if event.team_event:
            if event.event_type.type == '4':
                if userprofile.flagship:
                    if event.name == "Antarang":
                        userprofile.antarang = True
                    elif event.name == "Aayam":
                        userprofile.aayam = True
                    elif event.name == "Nrityansh":
                        userprofile.nrityansh = True
                    else:
                        userprofile.cob = True

                    userprofile.save()
                else:
                    return Response(data={"message": "Complete your payment before registering."}, status=status.HTTP_402_PAYMENT_REQUIRED)

            team = TeamRegistration.objects.create(
                leader=userprofile,
                name=request.data['team_name'],
                event=event
            )
            team.save()

            return Response(
                data={
                    "message": f"Registered for Event and Team {team.id} Created Successfully",
                    "team_id": team.id,
                    "team_name": team.name
                },
                status=status.HTTP_201_CREATED
            )

        return Response(data={"message": "Event Registered Successfully"}, status=status.HTTP_200_OK)


class UpdateTeamAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        leader = UserProfile.objects.get(user=user)
        team = TeamRegistration.objects.get(
            id=request.data['team_id']
        )
        if team.leader != leader:
            return Response("You are not the team leader", status=status.HTTP_403_FORBIDDEN)

        member = request.data['member']

        try:
            member = UserProfile.objects.get(registration_code=member)
        except Exception:
            return Response(data={"message": "This user does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if member.amount_paid:
            if team.event not in member.events_registered.all():
                member.events_registered.add(team.event)
                team.members.add(member)
            else:
                return Response(data={"message": "This user is already registered for this event."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(data={"message": "The user has not completed their payment."}, status=status.HTTP_402_PAYMENT_REQUIRED)

        team.save()

        return Response(data={"message": "Team member added successfully."}, status=status.HTTP_200_OK)


class DeleteTeamAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        leader = UserProfile.objects.get(user=user)
        team = TeamRegistration.objects.get(
            id=request.data['team_id']
        )
        event = team.event
        members = team.members.all()

        if team.leader != leader:
            return Response("You are not the team leader", status=status.HTTP_403_FORBIDDEN)

        for member in members:
            if event in member.events_registered.all():
                member.events_registered.remove(event)

        leader.events_registered.remove(event)

        team.delete()

        return Response({"message": "Team Deleted Successfully"}, status=status.HTTP_200_OK)


class TeamDetailsAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        leader = UserProfile.objects.get(user=user)
        team = TeamRegistration.objects.get(
            id=request.data['team_id']
        )
        members = team.member_list

        data = {
            "team": {
                "id": team.id,
                "name": team.name,
                "leader": {
                    "id": leader.registration_code,
                    "name": leader.user.get_full_name()
                },
                "members": members
            }
        }

        return Response(data=data, status=status.HTTP_200_OK)
