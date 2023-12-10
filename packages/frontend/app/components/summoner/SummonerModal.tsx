import { Col, Container, Modal, Row } from "react-bootstrap";

import { SummonerModalProps } from "../../types";

export default function SummonerModal({
  showModal,
  onHide,
  name,
}: SummonerModalProps) {
  return (
    <Modal show={showModal} onHide={onHide} size="lg">
      <Modal.Header closeButton>
        <Container fluid>
          <Row>
            <Col>
              <Modal.Title>{name}</Modal.Title>
            </Col>
          </Row>
        </Container>
      </Modal.Header>
      <Modal.Body>body</Modal.Body>
    </Modal>
  );
}
