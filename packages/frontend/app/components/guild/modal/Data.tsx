import { useEffect, useState } from "react";
import { Card } from "react-bootstrap";

import { DataComponentProps } from "@/app/types";
import User from "./data/User";
import AddUser from "./data/AddUser";
import DelUser from "./data/DelUser";
import Region from "./data/Region";
import Setup from "./data/Setup";

export default function Data({ data, setGuild, setData }: DataComponentProps) {
  const [title, setTitle] = useState("");

  useEffect(() => {
    data.command === "user"
      ? setTitle(
          `${JSON.parse(data.body).name} ${
            JSON.parse(data.body).summonerLevel
          }`,
        )
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
      </Card.Body>
    </Card>
  );
}