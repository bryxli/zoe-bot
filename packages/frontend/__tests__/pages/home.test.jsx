import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Home from "@/page";

describe("Home", () => {
  beforeEach(() => {
    fetch.resetMocks();
  });

  it("renders Home", async () => {
    fetch.mockResponse(JSON.stringify(null));

    render(
      <AuthProvider>
        <GuildProvider>
          <Home />
        </GuildProvider>
      </AuthProvider>,
    );

    const component = screen.getByTestId("Home");

    expect(component).toBeInTheDocument();
  });
});
