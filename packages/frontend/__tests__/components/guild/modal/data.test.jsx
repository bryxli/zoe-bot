import "@testing-library/jest-dom";
import { act, render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Data from "@/components/guild/modal/Data";

describe("Data", () => {
  it("renders Data", async () => {
    const mockData = {
      command: "",
    };

    await act(async () => {
      render(
        <AuthProvider>
          <GuildProvider>
            <Data data={mockData} />
          </GuildProvider>
        </AuthProvider>,
      );
    });

    const component = screen.getByTestId("Data");

    expect(component).toBeInTheDocument();
  });
});
