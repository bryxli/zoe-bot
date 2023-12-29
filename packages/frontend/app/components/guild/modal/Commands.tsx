import { Card, Col, Row } from "react-bootstrap";

import { GuildCommandsProps } from "@/types";

export default function GuildCommands({
  guild,
  setGuild,
  setData,
}: GuildCommandsProps) {
  const addUser = () => {
    setData({ command: "adduser", body: { guildId: guild.guild_id } });
  };

  const delUser = () => {
    setData({ command: "deluser", body: { guildId: guild.guild_id } });
  };

  const region = () => {
    setData({ command: "region", body: { guildId: guild.guild_id } });
  };

  const setup = () => {
    setData({ command: "setup", body: { guildId: guild.guild_id } });
  };

  const reset = async () => {
    setData({
      command: "reset",
      body: { guildId: guild.guild_id, webhookId: guild.webhook_id },
    });
  };

  const acknowledge = async () => {
    if (!guild.acknowledgment) {
      const updatedGuild = await fetch("/api/dynamo/acknowledge", {
        method: "POST",
        body: JSON.stringify({
          guild: guild,
        }),
      }).then((result) => result.json());

      setGuild(updatedGuild);
    }
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
                /adduser
              </Card>
            ) : (
              <Card style={{ cursor: "pointer" }} onClick={addUser}>
                /adduser
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
            {guild.webhook_id === "" || !guild.acknowledgment ? (
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
            {guild.webhook_id === "" || !guild.acknowledgment ? (
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
            {guild.webhook_id === "" || guild.acknowledgment ? (
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
