import { Card, Col, Row } from "react-bootstrap";

import { GuildCommandsProps } from "@/app/types";

export default function GuildCommands({ guild, setGuild }: GuildCommandsProps) {
  // TODO: enable/disable based on if guild is setup
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

  const setup = () => {
    console.log("setup");
  };

  const reset = () => {
    console.log("reset");
  };

  const acknowledge = async () => {
    const updatedGuild = await fetch("/api/dynamo/acknowledge", {
      method: "POST",
      body: JSON.stringify({
        guild: guild,
      }),
    }).then((result) => result.json());

    setGuild(updatedGuild);
  };

  return (
    <Card>
      <Card.Header>
        <Card.Title>server commands</Card.Title>
      </Card.Header>
      <Card.Body className="text-center">
        <Row className="mt-1">
          <Col xs={3}>
            {guild.webhook_id !== "" ? (
              <Card
                style={{ backgroundColor: "#FE69B2", pointerEvents: "none" }}
              >
                /setup
              </Card>
            ) : (
              <Card style={{ cursor: "pointer" }} onClick={setup}>
                /setup
              </Card>
            )}
          </Col>
          <Col xs={3}>
            {guild.webhook_id === "" ? (
              <Card
                style={{ backgroundColor: "#FE69B2", pointerEvents: "none" }}
              >
                /addUser
              </Card>
            ) : (
              <Card style={{ cursor: "pointer" }} onClick={addUser}>
                /addUser
              </Card>
            )}
          </Col>
          <Col xs={3}>
            {guild.webhook_id === "" ? (
              <Card
                style={{ backgroundColor: "#FE69B2", pointerEvents: "none" }}
              >
                /deluser
              </Card>
            ) : (
              <Card style={{ cursor: "pointer" }} onClick={delUser}>
                /deluser
              </Card>
            )}
          </Col>
          <Col xs={3}>
            {guild.webhook_id === "" ? (
              <Card
                style={{ backgroundColor: "#FE69B2", pointerEvents: "none" }}
              >
                /region
              </Card>
            ) : (
              <Card style={{ cursor: "pointer" }} onClick={region}>
                /region
              </Card>
            )}
          </Col>
        </Row>
        <Row className="mt-3">
          <Col xs={3}>
            {guild.webhook_id === "" ? (
              <Card
                style={{ backgroundColor: "#FE69B2", pointerEvents: "none" }}
              >
                /reset
              </Card>
            ) : (
              <Card style={{ cursor: "pointer" }} onClick={reset}>
                /reset
              </Card>
            )}
          </Col>
          <Col xs={4}>
            {guild.webhook_id === "" ? (
              <Card
                style={{ backgroundColor: "#FE69B2", pointerEvents: "none" }}
              >
                /acknowledge
              </Card>
            ) : (
              <Card style={{ cursor: "pointer" }} onClick={acknowledge}>
                /acknowledge
              </Card>
            )}
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
}
