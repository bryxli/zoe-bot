import { useEffect, useState } from "react";
import { Card } from "react-bootstrap";

import { DataProps } from "@/app/types";

export default function Data(data: DataProps) {
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

  const addUser = () => {
    // call adduser api endpoint
  };

  const delUser = () => {
    // call deluser api endpoint
  };

  const region = () => {
    // call region api endpoint
  };

  const setup = () => {
    // call setup api endpoint
  };

  return (
    <Card className="h-100">
      <Card.Header
        className={data.command === "" ? "bg-transparent border-0" : ""}
      >
        <Card.Title>{title}</Card.Title>
      </Card.Header>
      <Card.Body>
        {data.command === "user" && <>{data.body}</>}
        {data.command === "adduser" && <>/adduser</>}
        {data.command === "deluser" && <>/deluser</>}
        {data.command === "region" && <>/region</>}
        {data.command === "setup" && <>/setup</>}
      </Card.Body>
    </Card>
  );
}
