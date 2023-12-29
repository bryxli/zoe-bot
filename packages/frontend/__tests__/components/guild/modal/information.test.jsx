import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import GuildInfo from "@/components/guild/modal/Information";

describe("GuildInfo", () => {
  it("renders GuildInfo", async () => {
    const mockGuild = {
      webhook_id: "",
    };

    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <GuildInfo guild={mockGuild} />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("GuildInfo");

    expect(component).toBeInTheDocument();
  });
});
