import { useEffect, useState } from "react";
import { Card, Row } from "react-bootstrap";

import { DynamoGuildProps } from "../../types";
import Summoner from "../summoner/Summoner";

export default function UserList(guild: DynamoGuildProps) {
  const [userlist, setUserlist] = useState<string[]>([]);

  useEffect(() => {
    const fetchSummonerNames = async (users: string[]) => {
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

    const dynamoUserList = guild.userlist || [];
    let userIds: string[] = [];

    dynamoUserList.forEach((user: any) => {
      userIds.push(Object.keys(user)[0]);
    });

    fetchSummonerNames(userIds);
  }, [guild]);

  return (
    <Card className="h-100">
      <Card.Header>
        <Card.Title>userlist</Card.Title>
      </Card.Header>
      <Card.Body>
        {userlist.length > 0 &&
          userlist.map(
            (user) =>
              user !== "" && (
                <Row className="mx-auto" key={user}>
                  <Summoner name={user} />
                </Row>
              ),
          )}
      </Card.Body>
      <Card.Footer className="bg-transparent">
        {userlist.length} players registered
      </Card.Footer>
    </Card>
  );
}
