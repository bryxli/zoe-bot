import { Card, Col, Row } from "react-bootstrap";

export default function GuildCommands() {
  // TODO: call api endpoints for respective functions
  const addUser = () => {
    console.log("adduser");
  };

  const delUser = () => {
    console.log("deluser");
  };

  const region = () => {
    console.log("region");
  };

  const reset = () => {
    console.log("reset");
  };

  const acknowledge = () => {
    console.log("acknowledge");
  };

  return (
    <Card>
      <Card.Header>
        <Card.Title>server commands</Card.Title>
      </Card.Header>
      <Card.Body className="text-center">
        <Row className="mt-1">
          <Col xs={3}>
            <Card style={{ cursor: "pointer" }} onClick={addUser}>
              /adduser
            </Card>
          </Col>
          <Col xs={3}>
            <Card style={{ cursor: "pointer" }} onClick={delUser}>
              /deluser
            </Card>
          </Col>
          <Col xs={3}>
            <Card style={{ cursor: "pointer" }} onClick={region}>
              /region
            </Card>
          </Col>
          <Col xs={3}>
            <Card style={{ cursor: "pointer" }} onClick={reset}>
              /reset
            </Card>
          </Col>
        </Row>
        <Row className="mt-3">
          <Col xs={4}>
            <Card style={{ cursor: "pointer" }} onClick={acknowledge}>
              /acknowledge
            </Card>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
}
