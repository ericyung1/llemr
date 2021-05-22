import axios from "axios";
import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import PatientOverview from "./PatientOverview";
import ActionsTable from "./ActionsTable";
import DemographicInfo from "./DemographicInfo";
import defineFields from "../functions/defineFields";
import defineOverviewFields from "../functions/defineOverviewFields";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

function PatientDetail(props) {
  const [loading, setLoading] = useState(true);
  const [fields, setFields] = useState({});

  const patientOverviewFields = defineOverviewFields(props);

  useEffect(() => {
    const apiUrl = `/api/patient/${props.pt_pk}`;
    const demographicUrl = "/api/demographic/" + props.pt_pk; //might need this to get other pt data
    axios.get(apiUrl).then((response) => {
      const data = response.data;
      setFields(defineFields(data));
      setLoading(false);
    });
  }, []);

  return (
    <Container>
      {loading ? (
        <span>Loading...</span>
      ) : (
        <>
          <Row>
            <Col>
              <PatientOverview
                fieldSet={patientOverviewFields}
                fields={fields}
              />
            </Col>
            <Col>
              <ActionsTable
                fieldSet={[
                  "new_note_url",
                  "new_referral_url",
                  "make_appointment_url",
                  "give_vaccine_url",
                  "upload_document_url",
                  "view_labs_url",
                ]}
                fields={fields}
              />
            </Col>
          </Row>
          <Row>
            <Col>
              <DemographicInfo fields={fields} />
            </Col>
          </Row>
        </>
      )}
    </Container>
  );
}

export default PatientDetail;
