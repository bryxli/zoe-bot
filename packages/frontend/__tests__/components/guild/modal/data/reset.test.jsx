import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Reset from "@/components/guild/modal/data/Reset";

describe("Reset", () => {
  it("renders Reset", async () => {
    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <Reset />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("Reset");

    expect(component).toBeInTheDocument();
  });
});
