import React, { useState } from 'react';
import axios from 'axios';
import Select from 'react-select';
import './Registration.css'; // Import your CSS file

const RegistrationForm = () => {
  //   const [formData, setFormData] = useState({
  //     fullName: '',
  //     email: '',
  //     phoneNumber: '',
  //     collegeName: '',
  //     collegeState: '',
  //     currentYear: '',
  //   });

  //   const handleInputChange = (name, value) => {
  //     setFormData((prevData) => ({
  //       ...prevData,
  //       [name]: value,
  //     }));
  //   };

  //   const handleSelectChange = (name, selectedOption) => {
  //     setFormData((prevData) => ({
  //       ...prevData,
  //       [name]: selectedOption.value,
  //     }));
  //   };

  //   const handleSubmit = async (e) => {
  //     e.preventDefault();

  //     try {
  //       const response = await axios.post('/api/submit-registration', formData);
  //       console.log('Form data submitted:', response.data);
  //       // Handle success, show a success message, or redirect the user
  //     } catch (error) {
  //       console.error('Error submitting form data:', error);
  //       // Handle error, show an error message, or redirect the user
  //     }
  //   };

  const collegeStates = [
    { value: '0', label: 'Andhra Pradesh' },
    { value: '1', label: 'Arunachal Pradesh' },
    { value: '2', label: 'Assam' },
    { value: '3', label: 'Bihar' },
    { value: '4', label: 'Chhattisgarh' },
    { value: '5', label: 'Goa' },
    { value: '6', label: 'Gujarat' },
    { value: '7', label: 'Haryana' },
    { value: '8', label: 'Himachal Pradesh' },
    { value: '9', label: 'Jharkhand' },
    { value: '10', label: 'Karnataka' },
    { value: '11', label: 'Kerala' },
    { value: '12', label: 'Madhya Pradesh' },
    { value: '13', label: 'Maharashtra' },
    { value: '14', label: 'Manipur' },
    { value: '15', label: 'Meghalaya' },
    { value: '16', label: 'Mizoram' },
    { value: '17', label: 'Nagaland' },
    { value: '18', label: 'Odisha' },
    { value: '19', label: 'Punjab' },
    { value: '20', label: 'Rajasthan' },
    { value: '21', label: 'Sikkim' },
    { value: '22', label: 'Tamil Nadu' },
    { value: '23', label: 'Telangana' },
    { value: '24', label: 'Tripura' },
    { value: '25', label: 'Uttar Pradesh' },
    { value: '26', label: 'Uttarakhand' },
    { value: '27', label: 'West Bengal' },
    { value: '28', label: 'Andaman and Nicobar Islands' },
    { value: '29', label: 'Chandigarh' },
    { value: '30', label: 'Dadra and Nagar Haveli and Daman and Diu' },
    { value: '31', label: 'Delhi' },
    { value: '32', label: 'Lakshadweep' },
    { value: '33', label: 'Puducherry' },
    // Add more states or UTs as needed
  ];

  const yearOptions = [
    { value: 'First Year', label: 'First Year' },
    { value: 'Second Year', label: 'Second Year' },
    { value: 'Third Year', label: 'Third Year' },
    { value: 'Fourth Year', label: 'Fourth Year' },
    { value: 'Fifth Year', label: 'Fifth Year' },
    { value: 'Other', label: 'Other' },
  ];

  return (
    <div className="container" >
      {/* <div className="form-container sign-up-container">
        <form action="#">
          <h1>Thank you for Registrations</h1>
        </form>
      </div> */}
      <div className="form-container sign-in-container">
        <form >
          <h1>Pre-Registration</h1>
          <input
            type="text"
            placeholder="Full Name"
            name="fullName"
            required
          // value={formData.fullName}
          // onChange={(e) => handleInputChange('fullName', e.target.value)}
          />
          <input
            type="email"
            placeholder="Email"
            name="email"
            pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            required
            // len
          // value={formData.email}
          // onChange={(e) => handleInputChange('email', e.target.value)}
          />
          <input
            type="tel"
            placeholder="Phone Number"
            name="phoneNumber"
            maxLength="10"
            minLength="10"
            required
            // value={formData.phoneNumber}
          // onChange={(e) => handleInputChange('phoneNumber', e.target.value)}
          />
          <input
            type="text"
            placeholder="College Name"
            name="collegeName"
            required
          // value={formData.collegeName}
          // onChange={(e) => handleInputChange('collegeName', e.target.value)}
          />
          <input
            type="text"
            placeholder="City"
            name="cityName"
            required
          // value={formData.collegeName}
          // onChange={(e) => handleInputChange('collegeName', e.target.value)}
          />
        
          <select name="state" id="state" placeholder="College State" required>
            <option value="" disabled selected>Choose College State</option>
            <option value="0">Andhra Pradesh</option>
            <option value="1">Arunachal Pradesh</option>
            <option value="2">Assam</option>
            <option value="3">Bihar</option>
            <option value="4">Chhattisgarh</option>
            <option value="5">Goa</option>
            <option value="6">Gujarat</option>
            <option value="7">Haryana</option>
            <option value="8">Himachal Pradesh</option>
            <option value="9">Jharkhand</option>
            <option value="10">Karnataka</option>
            <option value="11">Kerala</option>
            <option value="12">Madhya Pradesh</option>
            <option value="13">Maharashtra</option>
            <option value="14">Manipur</option>
            <option value="15">Meghalaya</option>
            <option value="16">Mizoram</option>
            <option value="17">Nagaland</option>
            <option value="18">Odisha</option>
            <option value="19">Punjab</option>
            <option value="20">Rajasthan</option>
            <option value="21">Sikkim</option>
            <option value="22">Tamil Nadu</option>
            <option value="23">Telangana</option>
            <option value="24">Tripura</option>
            <option value="25">Uttar Pradesh</option>
            <option value="26">Uttarakhand</option>
            <option value="27">West Bengal</option>
            <option value="28">Andaman and Nicobar Islands</option>
            <option value="29">Chandigarh</option>
            <option value="30">Dadra and Nagar Haveli and Daman and Diu</option>
            <option value="31">Daman and Diu</option>
            <option value="32">Lakshadweep</option>
            <option value="33">Delhi</option>
            <option value="34">Puducherry</option>
          </select>

          <select name="state" id="state" placeholder="College State" required>
            <option value="" disabled selected>Current Year</option>
            <option value="0">First Year</option>
            <option value="1">Second Year</option>
            <option value="2">Third Year</option>
            <option value="3">Fourth Year</option>
            <option value="4">Fifth Year</option>
            <option value="5">Other</option>
          </select>

          <button type="submit" className='ghost' id='signUp'>Submit</button>
        </form>
      </div>
      <div className="overlay-container">
        <div className="overlay">
          <div className="overlay-panel overlay-left"></div>
          <div className="overlay-panel overlay-right">
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegistrationForm;
