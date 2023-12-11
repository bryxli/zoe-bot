import { Button, Card, Col, Container, Modal, Row } from "react-bootstrap";

import { SummonerModalProps } from "@/app/types";

export default function SummonerModal({
  showModal,
  onHide,
  summoner,
}: SummonerModalProps) {
  const deleteUser = () => {
    console.log("deluser");
  };

  return (
    <Modal show={showModal} onHide={onHide} size="xl">
      <Modal.Header closeButton className="summoner">
        <Col xs={6}>{summoner.name}</Col>
        <Col>
          <div style={{ float: "right" }}>level {summoner.summonerLevel}</div>
        </Col>
      </Modal.Header>
      <Modal.Body className="summoner border-0">
        <Container className="full-height summoner border-0">
          <Button
            className="authButton"
            style={{ position: "absolute", bottom: 0 }}
            onClick={deleteUser}
          >
            delete user
          </Button>
        </Container>
      </Modal.Body>
      <Modal.Footer className="summoner border-0"></Modal.Footer>
    </Modal>
  );
}
