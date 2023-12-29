import "@testing-library/jest-dom";
import { render } from "@testing-library/react";

import { AuthProvider } from "@/contexts/AuthContext";
import { GuildProvider } from "@/contexts/GuildContext";
import Header from "@/components/Header";

describe("Header", () => {
  it("renders Header", () => {
    const container = render(
      <AuthProvider>
        <GuildProvider>
          <Header />
        </GuildProvider>
      </AuthProvider>,
    ).container;

    expect(container.getElementsByClassName("Header").length).toBe(1);
  });
});
