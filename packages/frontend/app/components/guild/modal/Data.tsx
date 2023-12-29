import { useEffect, useState } from "react";
import { Card } from "react-bootstrap";

import { DataComponentProps } from "@/types";

import User from "@/components/guild/modal/data/User";
import AddUser from "@/components/guild/modal/data/AddUser";
import DelUser from "@/components/guild/modal/data/DelUser";
import Region from "@/components/guild/modal/data/Region";
import Setup from "@/components/guild/modal/data/Setup";
import Reset from "@/components/guild/modal/data/Reset";

export default function Data({ data, setGuild, setData }: DataComponentProps) {
  const [title, setTitle] = useState("");

  useEffect(() => {
    data.command === "user"
      ? setTitle(`${data.body.name} ${data.body.summonerLevel}`)
      : setTitle(data.command);
  }, [data]);

  return (
    <Card className="h-100">
      <Card.Header
        className={data.command === "" ? "bg-transparent border-0" : ""}
      >
        <Card.Title>{title}</Card.Title>
      </Card.Header>
      <Card.Body>
        {data.command === "user" && (
          <User data={data} setGuild={setGuild} setData={setData} />
        )}
        {data.command === "adduser" && (
          <AddUser data={data} setGuild={setGuild} setData={setData} />
        )}
        {data.command === "deluser" && (
          <DelUser data={data} setGuild={setGuild} setData={setData} />
        )}
        {data.command === "region" && (
          <Region data={data} setGuild={setGuild} setData={setData} />
        )}
        {data.command === "setup" && (
          <Setup data={data} setGuild={setGuild} setData={setData} />
        )}
        {data.command === "reset" && (
          <Reset data={data} setGuild={setGuild} setData={setData} />
        )}
      </Card.Body>
    </Card>
  );
}
