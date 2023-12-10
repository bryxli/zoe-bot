import { Card } from "react-bootstrap";

import { SummonerProps } from "../../types";

export default function Summoner({ name }: SummonerProps) {
  // TODO: pass in respective data
  return (
    <Card style={{ cursor: "pointer" }}>
      <Card.Body>
        <Card.Title> {name} </Card.Title>
      </Card.Body>
    </Card>
  );
}
