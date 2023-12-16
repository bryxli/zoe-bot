import { Card, Row } from "react-bootstrap";

import { UserListProps } from "@/app/types";
import Summoner from "../summoner/Summoner";

export default function UserList({
  summoners,
  setGuild,
  setData,
}: UserListProps) {
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
              <Summoner summoner={summoner} setData={setData} />
            </Row>
          ))}
      </Card.Body>
      <Card.Footer className="bg-transparent">
        {summoners?.length || 0} players registered
      </Card.Footer>
    </Card>
  );
}
