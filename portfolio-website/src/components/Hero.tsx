import { Github, Linkedin, ExternalLink, Download } from "lucide-react";
import profile from "@/data/profile.json";

export default function Hero() {
  return (
    <section
      id="home"
      className="min-h-screen flex items-center justify-center relative overflow-hidden"
    >
      {/* Background grid */}
      <div
        className="absolute inset-0 opacity-10"
        style={{
          backgroundImage:
            "radial-gradient(circle at 1px 1px, rgb(99,102,241) 1px, transparent 0)",
          backgroundSize: "40px 40px",
        }}
      />

      {/* Glow blobs */}
      <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-600/20 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-72 h-72 bg-teal-600/20 rounded-full blur-3xl" />

      <div className="relative z-10 max-w-4xl mx-auto px-6 text-center">
        {/* Avatar placeholder */}
        <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-blue-500 to-teal-500 flex items-center justify-center text-3xl font-bold text-white shadow-lg">
          {profile.name.charAt(0)}
        </div>

        <p className="text-blue-400 font-medium tracking-widest uppercase text-sm mb-3">
          {profile.title}
        </p>

        <h1 className="text-5xl md:text-7xl font-extrabold mb-4 leading-tight">
          Hi, I&apos;m{" "}
          <span className="gradient-text">{profile.name.split(" ")[0]}</span>
        </h1>

        <p className="text-xl md:text-2xl text-slate-400 mb-8 max-w-2xl mx-auto">
          {profile.tagline}
        </p>

        <p className="text-slate-400 mb-10 max-w-xl mx-auto leading-relaxed">
          {profile.bio}
        </p>

        {/* CTA buttons */}
        <div className="flex flex-wrap justify-center gap-4 mb-10">
          <a
            href="#projects"
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors flex items-center gap-2"
          >
            View My Work
          </a>
          <a
            href={profile.resumeUrl}
            target="_blank"
            rel="noreferrer"
            className="px-6 py-3 border border-slate-600 hover:border-blue-500 rounded-lg font-semibold transition-colors flex items-center gap-2"
          >
            <Download size={16} /> Resume
          </a>
        </div>

        {/* Social links */}
        <div className="flex justify-center gap-5">
          <a href={profile.github} target="_blank" rel="noreferrer"
            className="text-slate-400 hover:text-white transition-colors">
            <Github size={22} />
          </a>
          <a href={profile.linkedin} target="_blank" rel="noreferrer"
            className="text-slate-400 hover:text-white transition-colors">
            <Linkedin size={22} />
          </a>
          <a href={profile.tableau} target="_blank" rel="noreferrer"
            className="text-slate-400 hover:text-white transition-colors">
            <ExternalLink size={22} />
          </a>
        </div>
      </div>
    </section>
  );
}
