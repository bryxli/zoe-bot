import { Card } from "react-bootstrap";

import { SummonerComponentProps } from "@/app/types";

export default function Summoner({
  summoner,
  setData,
}: SummonerComponentProps) {
  const display = () => {
    setData({ command: "user", body: JSON.stringify(summoner) });
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
    </>
  );
}
