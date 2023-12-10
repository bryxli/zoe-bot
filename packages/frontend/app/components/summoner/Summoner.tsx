import { useState } from "react";
import { Card } from "react-bootstrap";

import { SummonerProps } from "../../types";

import SummonerModal from "./Modal";

export default function Summoner(summoner: SummonerProps) {
  const [showModal, setShowModal] = useState(false);

  const display = () => {
    setShowModal(!showModal);
  };

  return (
    <>
      <Card
        style={{ cursor: "pointer" }}
        onClick={display}
        className="text-center mt-1"
      >
        {summoner.name}
      </Card>
      <SummonerModal
        showModal={showModal}
        onHide={display}
        summoner={summoner}
      />
    </>
  );
}
