import { Card } from "react-bootstrap";

import { SummonerComponentProps } from "@/types";

export default function Summoner({
  summoner,
  setData,
}: SummonerComponentProps) {
  const data = () => {
    setData({ command: "user", body: summoner });
  };

  return (
    <div data-testid="Summoner">
      <Card
        style={{ cursor: "pointer" }}
        onClick={data}
        className="text-center mt-1"
      >
        {summoner.name}
      </Card>
    </div>
  );
}
