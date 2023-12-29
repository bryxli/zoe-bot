import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import User from "@/components/guild/modal/data/User";

describe("User", () => {
  it("renders User", async () => {
    const mockData = {
      body: {
        id: "",
      },
    };

    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <User data={mockData} />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("User");

    expect(component).toBeInTheDocument();
  });
});
