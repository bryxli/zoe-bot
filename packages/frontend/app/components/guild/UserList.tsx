import { Card, Row } from "react-bootstrap";

import { UserlistProps } from "../../types";
import Summoner from "../summoner/Summoner";

export default function UserList({ userlist }: UserlistProps) {
  return (
    <Card className="h-100">
      <Card.Header>
        <Card.Title>userlist</Card.Title>
      </Card.Header>
      <Card.Body>
        {userlist.length > 0 ? (
          userlist.map((user) => {
            return (
              <Row className="mx-auto" key={user}>
                <Summoner name={user} />
              </Row>
            );
          })
        ) : (
          <Row className="mx-auto">userlist is empty</Row>
        )}
      </Card.Body>
    </Card>
  );
}
