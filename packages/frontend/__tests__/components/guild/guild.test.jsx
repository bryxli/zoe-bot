import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Guild from "@/components/guild/Guild";

describe("Guild", () => {
  beforeEach(() => {
    fetch.resetMocks();
  });

  it("renders Guild", async () => {
    const mockGuild = {
      userlist: [],
    };

    fetch.mockResponse(JSON.stringify(mockGuild));

    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <Guild />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("Guild");

    expect(component).toBeInTheDocument();
  });
});
