import { useEffect, useState } from "react";
import { Card } from "react-bootstrap";
import { DynamoGuildProps, GuildProps } from "@/app/types";
import GuildModal from "./Modal";

export default function Guild(props: GuildProps) {
  const [showModal, setShowModal] = useState(false);
  const [guild, setGuild] = useState<DynamoGuildProps>({
    acknowledgment: false,
    guild_id: "",
    region: "",
    userlist: [],
    webhook_id: "",
    webhook_url: "",
  });

  useEffect(() => {
    const fetchGuild = async () => {
      const guild = await fetch("/api/dynamo/guild", {
        method: "POST",
        body: JSON.stringify({
          guildId: props.id,
        }),
      }).then((result) => result.json());

      setGuild(guild);
    };

    fetchGuild();
  }, [props]);

  const display = () => {
    setShowModal(!showModal);
  };

  return (
    <>
      <Card className="h-100" style={{ cursor: "pointer" }} onClick={display}>
        <Card.Body className="d-flex align-items-center justify-content-center text-center">
          <Card.Title> {props.name} </Card.Title>
        </Card.Body>
      </Card>
      <GuildModal
        showModal={showModal}
        onHide={display}
        id={props.id}
        name={props.name}
        icon={props.icon}
        guild={guild}
      />
    </>
  );
}
