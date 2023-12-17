import { useEffect, useState } from "react";
import { Col, Container, Modal, Row } from "react-bootstrap";
import Image from "next/image";

import { DataProps, GuildModalProps } from "@/app/types";

import UserList from "./modal/UserList";
import GuildCommands from "./modal/Commands";
import GuildInfo from "./modal/Information";
import Data from "./modal/Data";

export default function GuildModal({
  showModal,
  onHide,
  id,
  name,
  icon,
  guild,
  setGuild,
  summoners,
}: GuildModalProps) {
  const [data, setData] = useState<DataProps>({
    command: "",
    body: "",
  });

  useEffect(() => {
    setData({
      command: "",
      body: "",
    });
  }, [showModal]);

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
        <Container className="full-height">
          <Row>
            <Col xs={8}>
              <GuildCommands
                guild={guild}
                setGuild={setGuild}
                setData={setData}
              />
              <br></br>
              <GuildInfo {...guild} />
            </Col>
            <Col xs={4}>
              <UserList summoners={summoners} setData={setData} />
            </Col>
          </Row>
          <br></br>
          <Row style={{ height: "21%" }}>
            <Col>
              <Data data={data} setGuild={setGuild} setData={setData} />
            </Col>
          </Row>
        </Container>
      </Modal.Body>
    </Modal>
  );
}
