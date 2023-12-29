import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Information from "@/components/Information";

describe("Information", () => {
  it("renders Information", () => {
    render(
      <AuthProvider>
        <GuildProvider>
          <Information />
        </GuildProvider>
      </AuthProvider>,
    );

    const component = screen.getByTestId("Information");

    expect(component).toBeInTheDocument();
  });
});
