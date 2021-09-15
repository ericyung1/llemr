import React from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

function DemographicInfo({ fields }) {
  return (
    <Container>
      <Row>
        <Col>
          <h3>Demographic Info</h3>
        </Col>
      </Row>
      <Row>
        <Col>
          <strong>Language: </strong>
          {fields.languages.value}
        </Col>
      </Row>
      <Row>
        <Col>
          <strong>DOB: </strong>
          {fields.date_of_birth.value}
        </Col>
      </Row>
      <Row>
        <Col>
          <strong>Email: </strong>
          {fields.email.value}
        </Col>
      </Row>
      <Row>
        <Col>
          <strong>Address: </strong>
          {fields.address.value} {fields.city.value}, {fields.state.value}{" "}
          {fields.zip_code.value}
        </Col>
      </Row>
      <Row>
        <Col>
          <table>
            <tr>
              <th>Contact</th>
              <th>Phone Number</th>
            </tr>
            {/* should redo this to make it cleaner later x[0] is phone number x[1] is name ex "Mobile" */}
            {fields.all_phones.value.map(
              (x, i) =>
                x[0] && (
                  <tr>
                    <td>{x[1] != "" ? x[1] : "Primary"}</td>
                    <td>{x[0]}</td>
                  </tr>
                )
            )}
          </table>
        </Col>
      </Row>
    </Container>
  );
}

export default DemographicInfo;
