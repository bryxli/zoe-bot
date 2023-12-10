import { DynamoGuildProps } from "../../types";
import { useEffect, useState } from "react";
import { Card, Row } from "react-bootstrap";

export default function GuildInfo(guild: DynamoGuildProps) {
  const [acknowledged, setAcknowledged] = useState(false);

  useEffect(() => {
    setAcknowledged(guild.acknowledgment || false);
  }, [guild]);

  return (
    <Card>
      <Card.Header>
        <Card.Title>guild info</Card.Title>
      </Card.Header>
      <Card.Body>
        <Row className="mx-auto">setup status</Row>
        <Row className="mx-auto">
          acknowledgement status:{" "}
          {acknowledged !== undefined && acknowledged.toString()}
        </Row>
        <Row className="mx-auto">current webhook location</Row>
        <Row className="mx-auto">current region location</Row>
        <Row className="mx-auto">number of registered players</Row>
      </Card.Body>
    </Card>
  );
}
