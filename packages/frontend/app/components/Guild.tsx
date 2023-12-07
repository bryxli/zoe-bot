"use client";

import { useState } from "react";
import { Card, Modal } from "react-bootstrap";
import Image from "next/image";

import { GuildProps } from "../types";

export default function Guild({
  id,
  name,
  icon,
  owner,
  permissions,
  permissions_new,
  features,
}: GuildProps) {
  const [showModal, setShowModal] = useState(false);

  const display = () => {
    setShowModal(!showModal);
  };

  return (
    <>
      <Card style={{ cursor: "pointer" }} onClick={display}>
        <Card.Body>
          <Card.Title> {name} </Card.Title>
        </Card.Body>
      </Card>

      <Modal show={showModal} onHide={display}>
        <Modal.Header closeButton>
          <Modal.Title> {name} </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Image
            src={`icons/${id}/${icon}.jpg`}
            alt="Guild Avatar"
            width={150}
            height={150}
            priority={true}
          />
        </Modal.Body>
      </Modal>
    </>
  );
}
