import React from "react";
import Container from "react-bootstrap/Container";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Button from "react-bootstrap/Button";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

function ActionsTable({ fields, fieldSet }) {
  const section = [];
  fieldSet.forEach((fieldName) => {
    section.push(fields[fieldName]);
  });

  return (
    <Container>
      <Row>
        <Col>
          <h3>Actions</h3>
          <h3>Clinic Day</h3>
        </Col>
      </Row>
      <Row>
        <Col>
          <ButtonGroup vertical>
            {section.map((field) => (
              <Button key={field.name} href={field.value}>
                {field.label}
              </Button>
            ))}
          </ButtonGroup>
        </Col>
      </Row>
    </Container>
  );
}

export default ActionsTable;
