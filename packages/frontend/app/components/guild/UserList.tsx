import { useEffect, useState } from "react";
import { Card, Row } from "react-bootstrap";

import { DynamoGuildProps } from "../../types";
import Summoner from "../summoner/Summoner";

export default function UserList(guild: DynamoGuildProps) {
  const [userlist, setUserlist] = useState<string[]>([]);

  useEffect(() => {
    const fetchUsers = async () => {
      // TODO: dont need to call api, can just use guild prop (this might be what is causing latency here)
      const users = await fetch("/api/dynamo/userlist", {
        method: "POST",
        body: JSON.stringify({
          guild: guild,
        }),
      }).then((result) => result.json());

      const summonerNames = await Promise.all(
        users.map(async (userId: string) => {
          return await fetch("/api/league/accountid", {
            method: "POST",
            body: JSON.stringify({
              accountId: userId,
            }),
          }).then((result) => result.json().then((response) => response.name));
        }),
      );
      setUserlist(summonerNames);
    };

    fetchUsers();
  }, [guild]);

  return (
    <Card className="h-100">
      <Card.Header>
        <Card.Title>userlist</Card.Title>
      </Card.Header>
      <Card.Body>
        {userlist.length > 0 ? (
          userlist.map(
            (user) =>
              user !== "" && (
                <Row className="mx-auto" key={user}>
                  <Summoner name={user} />
                </Row>
              ),
          )
        ) : (
          <Row className="mx-auto">userlist is empty</Row>
        )}
      </Card.Body>
      <Card.Footer className="bg-transparent">
        {userlist.length} players registered
      </Card.Footer>
    </Card>
  );
}
