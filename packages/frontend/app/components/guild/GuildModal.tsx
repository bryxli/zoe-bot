import { useEffect, useState } from "react";
import { Col, Container, Modal, Row } from "react-bootstrap";
import Image from "next/image";

import { GuildModalProps } from "../../types";

import UserList from "./UserList";
import GuildCommands from "./GuildCommands";
import GuildInfo from "./GuildInfo";

export default function GuildModal({
  showModal,
  onHide,
  id,
  name,
  icon,
}: GuildModalProps) {
  const [userlist, setUserlist] = useState<string[]>([]);

  useEffect(() => {
    const fetchUsers = async () => {
      const users = await fetch("/api/dynamo/userlist", {
        method: "POST",
        body: JSON.stringify({
          guildId: id,
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
  }, [id]);

  return (
    <Modal show={showModal} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Container fluid>
          <Row>
            <Col>
              <Modal.Title>{name}</Modal.Title>
            </Col>
            {icon && (
              <Col xs="auto">
                <Image
                  src={`https://cdn.discordapp.com/icons/${id}/${icon}.jpg`}
                  alt="Guild Avatar"
                  width={40}
                  height={40}
                  priority={true}
                />
              </Col>
            )}
          </Row>
        </Container>
      </Modal.Header>
      <Modal.Body>
        <Container fluid>
          <Row>
            <Col xs={8}>
              <Row>
                <GuildCommands />
              </Row>
              <Row className="mt-4">
                <GuildInfo />
              </Row>
            </Col>
            <Col xs={4}>
              <UserList userlist={userlist} />
            </Col>
          </Row>
        </Container>
      </Modal.Body>
    </Modal>
  );
}
