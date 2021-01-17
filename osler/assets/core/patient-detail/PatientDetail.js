import axios from 'axios';
import React, { useState, useEffect } from 'react';

function PatientDetail(props) {
  
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState([])

  useEffect(() => {
    const patientUrl = "/api/patient/" + props.pt_pk
    const demographicUrl = "/api/demographic/" + props.pt_pk
    async function getData() {
      const response = await axios(patientUrl)
      setData(response.data)
      setLoading(false)
    }
    if (loading) {
      getData();
    }
  }, []);

  return (
    <div>
      {loading ? (
        <p>Loading Please wait...</p>
      ) : (
      <div>
        <div className="jumbotron">
          <div className="container">
            <div class="col-lg-5 col-lg-offset-1 col-sm-6">
              <div class="col-md-1">
                <h2><br /><a href="/core/all/"><span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span></a></h2>
              </div>
              <div class="col-md-11">
                <h2> <a href={data["update_url"]}>{data["name"]}</a></h2>
                <p class="lead">{data["age"]} y/o  {data["ethnicities"].join(", ")}  {data["gender"].toLowerCase()}</p>
                <p class="lead"><strong>Action Items:</strong> {data["actionitem_status"]} </p>
                {props.displayReferrals && 
                  <p class="lead"><strong>FQHC Referral Status:</strong>  referral_status </p>
                }
                {props.displayReferrals && 
                  <p class="lead"><strong>Referrals:</strong>  referrals.iterator | join:", " </p>
                }
                {props.displayCaseManagers && 
                  <p class="lead"><strong>Case Manager:</strong> patient.case_managers.iterator | join:"; "</p>
                }
                <p class="lead"> <strong>Status:</strong> {data["status"]}
                % if can_activate %
                <a href={data["activate_url"]}><span class="glyphicon glyphicon-remove-circle" aria-hidden="true"></span></a>
                % endif %</p>
                {data["pending_workup_set"].length > 0 &&
                  <div class="alert alert-danger" role="alert">
                    Patient has a <a class="alert-link" href="% url 'workup' workup.pk %}">pending workup.</a>
                  </div>
                } 
              </div>
            </div>
            <div className="col-lg-offset-1 col-lg-4 col-sm-6 text-center" style={{border: "2px black"}}>
              <h3> Actions </h3>
              <div class="panel panel-primary">
                <div class="panel-heading">
                  <h3 class="panel-title">Clinic Day</h3>
                </div>
                <ul class="list-group">
                  <li class="list-group-item">
                    <span class="glyphicon glyphicon-search" aria-hidden="true"></span>&nbsp;
                    <a href={data["new_note_url"]}><strong>Write Note</strong></a>
                  </li>
                  {props.displayReferrals && 
                  <li class="list-group-item">
                    <span class="glyphicon glyphicon-transfer" aria-hidden="true"></span>&nbsp;
                    <a href={data["new_referral_url"]}><strong>Make Referral</strong></a>
                  </li>
                  }
                  {props.displayAppointments && 
                  <li class="list-group-item">
                    <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>&nbsp;
                    <a href={data["make_appointment_url"]}><strong>Make Appointment</strong></a>
                  </li>
                  }
                  {props.displayVaccine && 
                  <li class="list-group-item">
                    <span class="glyphicon glyphicon-pushpin" aria-hidden="true"></span>&nbsp;
                    <a href={data["give_vaccine_url"]}><strong>Give Vaccine</strong></a>
                  </li>
                  }
                  <li class="list-group-item">
                    <span class="glyphicon glyphicon-paperclip" aria-hidden="true"></span>&nbsp;
                    <a href={data["upload_document_url"]}><strong>Upload Document</strong></a>
                  </li>
                  <li class="list-group-item">
                    <span class="glyphicon glyphicon-tint" aria-hidden="true"></span>&nbsp;
                      <a href={data["view_labs_url"]}><strong>View Labs</strong></a>
                  </li>
                </ul>
              </div>

              <div class="panel panel-success">
                <div class="panel-heading">
                  <h3 class="panel-title">Followup</h3>
                </div>
                <ul class="list-group">
                {props.displayReferrals && 
                  <li class="list-group-item">
                    <span class="glyphicon glyphicon-phone-alt" aria-hidden="true"></span>&nbsp;
                    <a href={data["log_followup_url"]}><strong>Log follow up</strong> (referral)</a>
                  </li>
                  }
                  <li class="list-group-item">
                    <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>&nbsp;
                    <a href={data["new_ai_url"]}><strong>New Action Item</strong></a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div class="container">
          <h3>&nbsp;&nbsp;Demographic Information</h3>
          <div class="container col-md-4">
            <p><strong>&nbsp;&nbsp;Language:</strong>  {data["languages"].join(", ")} </p>
            <p><strong>&nbsp;&nbsp;DOB:</strong> {data["date_of_birth"]}</p>
            <p><strong>&nbsp;&nbsp;Email:</strong> {data["email"] || "Not Provided"}</p>
          </div>
          <div class="container col-md-4">
            <p>
              <strong>Address:</strong><br />
              {data["address"]} <br />
              {data["city"]}, {data["state"]} {data["zip_code"]}
            </p>
          </div>
          <div class="container col-md-4">
            <table class="table table-condensed">
              <tr>
                <th>Contact</th>
                <th>Phone Number</th>
              </tr>
              {/* should redo this to make it cleaner later x[0] is phone number x[1] is name ex "Mobile" */}
              {data["all_phones"].map((x,i) => 
               x[0]  && <tr><td>{x[1] != "" ? x[1] : "Primary"}</td><td>{x[0]}</td></tr>
              )}
            </table>
          </div>
        </div>
        <div class="container">
          <div class="col-md-8 col-md-offset-2">
            {data["demographics"] ? 
            <a href="{% url 'demographics-detail' patient.demographics.id %}" class="btn btn-default" role="button">See Patient Survey Data</a>
            :
            <div class="alert alert-danger" role="alert">
              No survey data exists for this patient. Please <a class="alert-link" href={data["demographics_create_url"]}>click here <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></a> to add it.</div>
            }
          </div>
        </div>
        <div class="container">
          <div class="col-md-6">
            <h3>Submitted Notes ({data["notes"].length}  Total)</h3>
          </div>
        </div>
      </div>
      )}
    </div>
  );

}


export default PatientDetail;

