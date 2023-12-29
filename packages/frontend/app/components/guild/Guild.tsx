import { useEffect, useState } from "react";
import { Card } from "react-bootstrap";

import { DynamoGuildProps, GuildProps, SummonerProps } from "@/types";

import GuildModal from "@/components/guild/Guild";

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
  const [summoners, setSummoners] = useState<SummonerProps[]>([]);
  const [webhookLocation, setWebhookLocation] = useState("");

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

  useEffect(() => {
    const fetchSummoners = async (users: string[]) => {
      const summoners = await Promise.all(
        users.map(async (userId: string) => {
          return await fetch("/api/league/accountid", {
            method: "POST",
            body: JSON.stringify({
              accountId: userId,
              region: guild.region,
            }),
          }).then((result) => result.json());
        }),
      );
      setSummoners(summoners);
    };

    const setLocation = async () => {
      const webhook = await fetch("/api/discord/webhook/details", {
        method: "POST",
        body: JSON.stringify({
          guild: guild,
        }),
      }).then((result) => result.json());

      setWebhookLocation(webhook);
    };

    const dynamoUserList = guild.userlist || [];
    let userIds: string[] = [];

    dynamoUserList.forEach((user) => {
      userIds.push(Object.keys(user)[0]);
    });

    fetchSummoners(userIds);
    setLocation();
  }, [guild]);

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
        setGuild={setGuild}
        summoners={summoners}
        location={webhookLocation}
      />
    </>
  );
}
