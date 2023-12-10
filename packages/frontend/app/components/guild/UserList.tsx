import { useEffect, useState } from "react";
import { Card, Row } from "react-bootstrap";

import { DynamoGuildProps, SummonerProps } from "../../types";
import Summoner from "../summoner/Summoner";

export default function UserList(guild: DynamoGuildProps) {
  const [userlist, setUserlist] = useState<string[]>([]);
  const [summoners, setSummoners] = useState<SummonerProps[]>();

  useEffect(() => {
    const fetchSummoners = async (users: string[]) => {
      const summoners = await Promise.all(
        users.map(async (userId: string) => {
          return await fetch("/api/league/accountid", {
            method: "POST",
            body: JSON.stringify({
              accountId: userId,
            }),
          }).then((result) => result.json());
        }),
      );
      setSummoners(summoners);
    };

    const dynamoUserList = guild.userlist || [];
    let userIds: string[] = [];

    dynamoUserList.forEach((user) => {
      userIds.push(Object.keys(user)[0]);
    });

    fetchSummoners(userIds);
  }, [guild]);

  useEffect(() => {
    summoners && setUserlist(summoners?.map((summoner) => summoner.name));
  }, [summoners]);

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
        {userlist.length} players registered
      </Card.Footer>
    </Card>
  );
}
