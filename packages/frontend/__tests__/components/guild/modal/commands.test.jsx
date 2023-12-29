import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import GuildCommands from "@/components/guild/modal/Commands";

describe("GuildCommands", () => {
  it("renders GuildCommands", async () => {
    const mockGuild = {
      webhook_id: "",
    };

    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <GuildCommands guild={mockGuild} />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("GuildCommands");

    expect(component).toBeInTheDocument();
  });
});
