import { Button, Col, Container, Modal, Row } from "react-bootstrap";

import { SummonerModalProps } from "../../types";

export default function SummonerModal({
  showModal,
  onHide,
  name,
}: SummonerModalProps) {
  const deleteUser = () => {
    console.log("deluser");
  };

  return (
    <Modal show={showModal} onHide={onHide} fullscreen={true}>
      <Modal.Header closeButton>
        <Container fluid>
          <Row>
            <Col>
              <Modal.Title>{name}</Modal.Title>
            </Col>
          </Row>
        </Container>
      </Modal.Header>
      <Modal.Body>
        <Container className="d-flex flex-column align-items-center justify-content-center mb-4">
          <Row>dummy</Row>
          <Button className="mt-3" onClick={deleteUser}>
            delete user
          </Button>
        </Container>
      </Modal.Body>
    </Modal>
  );
}
