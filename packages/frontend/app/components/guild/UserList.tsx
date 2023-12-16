import { useEffect, useState } from "react";
import { Card, Row } from "react-bootstrap";

import { SummonerProps } from "@/app/types";
import Summoner from "../summoner/Summoner";

export default function UserList(props: SummonerProps[]) {
  const [summoners, setSummoners] = useState<SummonerProps[]>([]);

  useEffect(() => {
    const summoners = Object.values(props);
    setSummoners(summoners);
  }, [props]);

  return (
    <Card className="h-100">
      <Card.Header>
        <Card.Title>userlist</Card.Title>
      </Card.Header>
      <Card.Body>
        {summoners &&
          summoners.length > 0 &&
          summoners.map((summoner) => (
            <Row key={summoner.name}>
              <Summoner {...summoner} />
            </Row>
          ))}
      </Card.Body>
      <Card.Footer className="bg-transparent">
        {summoners?.length || 0} players registered
      </Card.Footer>
    </Card>
  );
}
