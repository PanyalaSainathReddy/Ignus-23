from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
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
    permission_classes = [AllowAny]
    serializer_class = EventTypeSerializer
    model = EventType

    def get(self, request, reference_name):
        # try:
        #     user = request.user
        #     user = User.objects.get(id=user.id)
        #     userprofile = UserProfile.objects.get(user=user)
        # except Exception:
        #     pass

        queryset = EventType.objects.get(reference_name=reference_name)

        serializer = EventTypeSerializer(queryset)
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

        unregistered = []
        unpaid = []
        paid = []
        already = []

        for member in request.data['members']:
            try:
                mem = UserProfile.objects.get(registration_code=member)

                if mem.amount_paid:
                    if team.event not in mem.events_registered:
                        paid.append(mem)
                    else:
                        already.append(mem)
                else:
                    unpaid.append(mem)
            except Exception:
                unregistered.append(mem)

        for member in paid:
            member.events_registered.add(team.event)
            team.members.add(member)

        team.update()

        data = {
            "paid": [member.registration_code for member in paid],
            "already": [member.registration_code for member in already],
            "unpaid": [member.registration_code for member in unpaid],
            "unregistered": [member.registration_code for member in unregistered]
        }

        if already is None and unpaid is None and unregistered is None:
            data["message"] = "Team Member(s) Added Successfully"

        return Response(data=data, status=status.HTTP_200_OK)


class DeleteTeamAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        leader = UserProfile.objects.get(user=user)
        team = TeamRegistration.objects.get(
            id=request.data['team_id']
        )
        if team.leader != leader:
            return Response("You are not the team leader", status=status.HTTP_403_FORBIDDEN)

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
