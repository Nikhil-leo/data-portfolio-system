import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import About from "@/components/About";
import Skills from "@/components/Skills";
import Projects from "@/components/Projects";
import Dashboards from "@/components/Dashboards";
import Resume from "@/components/Resume";
import Contact from "@/components/Contact";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Navbar />
      <div className="pt-16">
        <Hero />
        <About />
        <Skills />
        <Projects />
        <Dashboards />
        <Resume />
        <Contact />
        <Footer />
      </div>
    </main>
  );
}
