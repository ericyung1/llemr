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
          <div>
          <p>REACT STUFF</p>
          <p>Last Name: {data["last_name"]}</p>
          </div>
      )}
    </div>
  );

}


export default PatientDetail;
