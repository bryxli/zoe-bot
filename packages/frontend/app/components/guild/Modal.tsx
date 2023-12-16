import { Col, Container, Modal, Row } from "react-bootstrap";
import Image from "next/image";

import { GuildModalProps } from "@/app/types";

import UserList from "./UserList";
import GuildCommands from "./Commands";
import GuildInfo from "./Information";
import Output from "./Output";

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
        <Container fluid className="full-height">
          <Row>
            <Col xs={8}>
              <GuildCommands guild={guild} setGuild={setGuild} />
              <br></br>
              <GuildInfo {...guild} />
            </Col>
            <Col xs={4}>
              <UserList summoners={summoners} setGuild={setGuild} />
            </Col>
          </Row>
          <br></br>
          <Row style={{ height: "45%" }}>
            <Col>
              <Output />
            </Col>
          </Row>
        </Container>
      </Modal.Body>
    </Modal>
  );
}
