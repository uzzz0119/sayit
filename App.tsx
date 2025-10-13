import { useState } from "react";
import { NoteGenerator } from "./components/NoteGenerator";
import { NoteStorage } from "./components/NoteStorage";
import { LearningArea } from "./components/LearningArea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Toaster } from "./components/ui/sonner";

interface Note {
  id: string;
  title: string;
  content: string;
  createdAt: string;
  source?: string;
}

export default function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);

  const handleNoteGenerated = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  const handleSelectNote = (note: Note) => {
    setSelectedNote(note);
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto py-12 px-4 max-w-5xl">
        {/* Vintage Header */}
        <div className="mb-12 text-center relative">
          {/* Hand-drawn doodles - positioned to not overlap text */}
          <div className="float-doodle" style={{ position: 'absolute', top: '0', left: '10%', fontSize: '1.5rem', opacity: '0.6', animationDelay: '0.5s' }}>✦</div>
          <div className="float-doodle" style={{ position: 'absolute', top: '0', right: '10%', fontSize: '1.5rem', opacity: '0.6', animationDelay: '1s' }}>✧</div>
          
          <h1 className="text-5xl mb-4 tracking-tight inline-block relative z-10" style={{ fontFamily: "'DM Serif Display', serif" }}>
            SayIt
          </h1>
          <p className="text-lg mb-12 relative z-10" style={{ letterSpacing: '0.05em' }}>
            Say it. Learn it. Own it.
          </p>
        </div>

        {/* Tabs with vintage style */}
        <Tabs defaultValue="generator" className="space-y-8">
          <TabsList className="grid w-full grid-cols-3 bg-card border-2 border-foreground p-1.5 h-auto rounded-xl shadow-md">
            <TabsTrigger 
              value="generator"
              className="data-[state=active]:bg-foreground data-[state=active]:text-primary-foreground border-2 border-transparent data-[state=active]:border-foreground py-3 rounded-lg transition-all data-[state=active]:shadow-md"
            >
              笔记生成
            </TabsTrigger>
            <TabsTrigger 
              value="storage"
              className="data-[state=active]:bg-foreground data-[state=active]:text-primary-foreground border-2 border-transparent data-[state=active]:border-foreground py-3 rounded-lg transition-all data-[state=active]:shadow-md"
            >
              笔记存储
            </TabsTrigger>
            <TabsTrigger 
              value="learning"
              className="data-[state=active]:bg-foreground data-[state=active]:text-primary-foreground border-2 border-transparent data-[state=active]:border-foreground py-3 rounded-lg transition-all data-[state=active]:shadow-md"
            >
              强化学习
            </TabsTrigger>
          </TabsList>

          <TabsContent value="generator" className="relative">
            <div className="absolute top-2/3 -right-16 text-2xl opacity-40 pointer-events-none float-doodle" style={{ animationDelay: '0s' }}>✎</div>
            <NoteGenerator onNoteGenerated={handleNoteGenerated} />
          </TabsContent>

          <TabsContent value="storage" className="relative">
            <div className="absolute top-1/2 -left-16 text-2xl opacity-40 pointer-events-none float-doodle" style={{ animationDelay: '0.5s' }}>❋</div>
            <div className="absolute bottom-1/4 -right-16 text-xl opacity-30 pointer-events-none float-doodle" style={{ animationDelay: '1s' }}>✦</div>
            <NoteStorage 
              refreshTrigger={refreshTrigger} 
              onSelectNote={handleSelectNote}
            />
          </TabsContent>

          <TabsContent value="learning" className="relative">
            <div className="absolute top-2/3 -right-16 text-2xl opacity-40 pointer-events-none float-doodle" style={{ animationDelay: '1.5s' }}>✦</div>
            <LearningArea selectedNote={selectedNote} />
          </TabsContent>
        </Tabs>

        {/* Vintage Footer */}
        <div className="mt-16 pt-8 border-t-2 border-dashed border-foreground/30 text-center relative">
          <div className="float-doodle" style={{ position: 'absolute', right: '30%', top: '-15px', fontSize: '1.5rem', opacity: '0.6', animationDelay: '1.5s' }}>❋</div>
          <p className="text-sm text-muted-foreground">
            Made for English learners ♡
          </p>
        </div>
      </div>
      
      <Toaster />
    </div>
  );
}
