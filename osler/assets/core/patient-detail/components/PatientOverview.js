import React from "react";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";

function PatientOverview({ fields, fieldSet }) {
  const section = [];
  fieldSet.forEach((fieldName) => {
    section.push(fields[fieldName]);
  });

  return (
    <Container>
      <Row>
        <Col>
          <h2>
            <a href={fields.update_url.value}>{fields.name.value}</a>
          </h2>
        </Col>
      </Row>
      <Row>
        <Col>
          {fields.age.value} y/o {fields.ethnicities.value}{" "}
          {fields.gender.value}
        </Col>
      </Row>
      {section.map((field) => (
        <Row key={field.name}>
          <Col>
            <strong>{field.name}: </strong>
            {field.value ? field.value : "(empty)"}
          </Col>
        </Row>
      ))}
    </Container>
  );
}

export default PatientOverview;
