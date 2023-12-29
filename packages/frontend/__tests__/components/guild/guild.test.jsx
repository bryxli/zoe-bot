import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Guild from "@/components/guild/Guild";

describe("Guild", () => {
  beforeEach(() => {
    fetch.resetMocks();
  });

  it("renders Guild", async () => {
    fetch.mockResponse(JSON.stringify(null));

    render(
      <AuthProvider>
        <GuildProvider>
          <Guild />
        </GuildProvider>
      </AuthProvider>,
    );

    const component = screen.getByTestId("Guild");

    expect(component).toBeInTheDocument();
  });
});
