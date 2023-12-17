import { DynamoGuildProps } from "@/app/types";
import { useEffect, useState } from "react";
import { Card, Row } from "react-bootstrap";

export default function GuildInfo(guild: DynamoGuildProps) {
  const [setup, setSetup] = useState(false);
  const [webhookLocation, setWebhookLocation] = useState("");
  const [region, setRegion] = useState("");
  const [acknowledged, setAcknowledged] = useState(false);

  useEffect(() => {
    const setLocation = async () => {
      const webhook = await fetch("/api/discord/webhook/details", {
        method: "POST",
        body: JSON.stringify({
          guild: guild,
        }),
      }).then((result) => result.json());

      setWebhookLocation(webhook);
    };

    setLocation();
    setSetup(guild.guild_id !== "" && guild.guild_id !== undefined);
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
        <Row className="mx-auto">
          current webhook location: {webhookLocation}
        </Row>
        <Row className="mx-auto">current region location: {region}</Row>
        <Row className="mx-auto">
          acknowledgement status:{" "}
          {acknowledged !== undefined && acknowledged.toString()}
        </Row>
      </Card.Body>
    </Card>
  );
}
