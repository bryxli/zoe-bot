import { useEffect, useState } from "react";
import { Card, Row } from "react-bootstrap";

import { GuildInfoProps } from "@/types";

export default function GuildInfo({ guild, location }: GuildInfoProps) {
  const [setup, setSetup] = useState(false);
  const [region, setRegion] = useState("");
  const [acknowledged, setAcknowledged] = useState(false);

  useEffect(() => {
    setSetup(guild.webhook_id !== "" && guild.webhook_id !== undefined);
    setAcknowledged(guild.acknowledgment || false);
  }, [guild]);

  useEffect(() => {
    setup && setRegion(guild.region);
  }, [guild, setup]);

  return (
    <Card>
      <Card.Header>
        <Card.Title>guild info</Card.Title>
      </Card.Header>
      <Card.Body>
        <Row className="mx-auto">
          setup status: {setup !== undefined && setup.toString()}
        </Row>
        <Row className="mx-auto">current webhook location: {location}</Row>
        <Row className="mx-auto">current region location: {region}</Row>
        <Row className="mx-auto">
          acknowledgement status:{" "}
          {acknowledged !== undefined && acknowledged.toString()}
        </Row>
      </Card.Body>
    </Card>
  );
}
