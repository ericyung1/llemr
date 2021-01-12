import axios from 'axios';
import React, { useState, useEffect } from 'react';



function PatientDetail() {
  
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState([])

  

  useEffect(() => {
    const pt_pk = document.getElementById("SPECIAL").getAttribute("data-info")
    //ALTERNATE SOLUTION
    // const curr_url = document.location.href
    // const pt_pk = curr_url.slice(curr_url.length-2,curr_url.length-1) //lazy string manip rn
    async function getData() {
      await axios
        .get(`/api/patient/${pt_pk}`)  
        .then((response) => {
          // check if the data is populated
          console.log(response.data);
          setData(response.data);
          // you tell it that you had the result
          setLoading(false);
        });
    }
    if (loading) {
      // if the result is not ready so you make the axios call
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
