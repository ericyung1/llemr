import axios from 'axios';
import React, { useState, useEffect } from 'react';



function PatientDetail(props) {
  
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState([])

  useEffect(() => {
    let apiUrl = "/api/patient/" + props.pt_pk
    async function getData() {
      await axios
        .get(apiUrl)  
        .then((response) => {
          setData(response.data);
          setLoading(false);
        });
    }
    if (loading) {
      getData();
    }
  }, []);

  return (
    <div>
      {/* here you check if the state is loading otherwise if you will not call that you will get a blank page because the data is an empty array at the moment of mounting */}
      {loading ? (
        <p>Loading Please wait...</p>
      ) : (
          <div class="container">
            <h3>Demographic Information</h3>
            <div class="container col-md-4">
              <p>
                <strong>Language: </strong> {data["languages"][0]}
              </p>
              <p>
                <strong>DOB: </strong> {data["date_of_birth"]}
              </p>
              <p>
                <strong>Email: </strong> {data["email"] || "Not provided"}
              </p>
            </div>
            <div class="container col-md-4">
              <p>
                <strong>Address: </strong>
              </p>
              <p>
                {data["address"]}
              </p>
              <p>
                {data["city"]}, {data["state"]}
              </p>
            </div>
            <div class="container col-md-4">
              <p>
                <strong>Phone: </strong> {data["phone"]}
              </p>
            </div>
          </div>
      )}
    </div>
  );

}


export default PatientDetail;
