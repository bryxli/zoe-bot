import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Summoner from "@/components/guild/modal/summoner/Summoner";

describe("Summoner", () => {
  it("renders Summoner", async () => {
    const mockSummoner = {
      name: "",
    };

    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <Summoner summoner={mockSummoner} />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("Summoner");

    expect(component).toBeInTheDocument();
  });
});
