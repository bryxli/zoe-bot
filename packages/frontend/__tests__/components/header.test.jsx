import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Header from "@/components/Header";

describe("Header", () => {
  it("renders Header", () => {
    render(
      <AuthProvider>
        <GuildProvider>
          <Header />
        </GuildProvider>
      </AuthProvider>,
    );

    const component = screen.getByTestId("Header");

    expect(component).toBeInTheDocument();
  });
});
