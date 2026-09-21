import React from 'react';
import {Composition, Folder} from 'remotion';
import {WalkerGodotSetup, walkerGodotSetupSchema} from './scenes/WalkerGodotSetup';
import {GodotDevWorkbench, godotDevWorkbenchSchema} from './scenes/GodotDevWorkbench';
import {GodotDesignBoard, godotDesignBoardSchema} from './scenes/GodotDesignBoard';
import {GodotDesignFigure, godotDesignFigureSchema} from './scenes/GodotDesignFigure';
import {BarChart, barChartSchema} from './scenes/BarChart';
import {OutroSeries, outroSeriesSchema} from './scenes/OutroSeries';
import {OutroCTA, outroCtaSchema} from './scenes/OutroCTA';
import {BrutalistTerminalOpen, brutalistTerminalOpenSchema} from './scenes/BrutalistTerminalOpen';
import {BrutalistAdaptCLI, brutalistAdaptCLISchema} from './scenes/BrutalistAdaptCLI';
import {BrutalistCommentCTA, brutalistCommentCTASchema} from './scenes/BrutalistCommentCTA';
import {MedhavyTerminalAsk, medhavyTerminalAskSchema} from './scenes/MedhavyTerminalAsk';
import {MedhavyCodeBlock, medhavyCodeBlockSchema} from './scenes/MedhavyCodeBlock';
import {MedhavyOpen, medhavyOpenSchema} from './scenes/MedhavyOpen';
import {MedhavyOutro, medhavyOutroSchema} from './scenes/MedhavyOutro';
import {SeisSpotlightOpen, seisSpotlightOpenSchema} from './scenes/SeisSpotlightOpen';
import {SeisCard, seisCardSchema} from './scenes/SeisCard';
import {SeisProfileCredit, seisProfileCreditSchema} from './scenes/SeisProfileCredit';
import {SeisOutro, seisOutroSchema} from './scenes/SeisOutro';
import {SeisTribute, seisTributeSchema} from './scenes/SeisTribute';
import {SeisShowcase, seisShowcaseSchema} from './scenes/SeisShowcase';
import {SeisWall, seisWallSchema} from './scenes/SeisWall';
import {SeisStoriesRoll, seisStoriesRollSchema} from './scenes/SeisStoriesRoll';
import {SeisReadAlong, seisReadAlongSchema} from './scenes/SeisReadAlong';
import {SeisSongReadAlong, seisSongReadAlongSchema} from './scenes/SeisSongReadAlong';
import {SeisQA, seisQASchema} from './scenes/SeisQA';
import {SeisFilm, seisFilmSchema} from './scenes/SeisFilm';
import {SeisLogoTechnique, seisLogoTechniqueSchema} from './scenes/SeisLogoTechnique';
import {NikBearBrownOpen, nikBearBrownOpenSchema} from './scenes/NikBearBrownOpen';
import {NikBearBrownOutro, nikBearBrownOutroSchema} from './scenes/NikBearBrownOutro';
import {NikBearBrownTerminalAsk, nikBearBrownTerminalAskSchema} from './scenes/NikBearBrownTerminalAsk';
import {NikBearBrownCodeBlock, nikBearBrownCodeBlockSchema} from './scenes/NikBearBrownCodeBlock';
import {ClaudeComposerAsk, claudeComposerAskSchema} from './scenes/ClaudeComposerAsk';
// SlateCard DELETED 2026-08-30 — DESIGN-PRINCIPLES §1 banned card (eyebrow/kicker +
// bold sans headline + rule + decorative circle). Replaced by the two accepted forms.
import {FormACard, formACardSchema} from './scenes/FormACard';
import {TypesetMath, typesetMathSchema} from './scenes/TypesetMath';
import {ExecutedData, executedDataSchema} from './scenes/ExecutedData';
import {FormBCard, formBCardSchema} from './scenes/FormBCard';
import {FormACard916, formACard916Schema} from './scenes/FormACard916';
import {FormBCard916, formBCard916Schema} from './scenes/FormBCard916';
// Ported from the sandbox 2026-08-30 — components the public skills already name.
import {ClaudeMascotGrid, claudeMascotGridSchema} from './scenes/ClaudeMascotGrid';
import { ClaudeMascotShortGrid, claudeMascotShortGridSchema } from './scenes/ClaudeMascotShortGrid';
import {ClaudeMascotScene, claudeMascotSceneSchema} from './scenes/ClaudeMascotScene';
import {DoodleChart, doodleChartSchema} from './scenes/DoodleChart';
import {DoodleScene, doodleSceneSchema} from './scenes/DoodleScene';
import {GitHubSectionRail, gitHubSectionRailSchema} from './scenes/GitHubSectionRail';
import {GitHubStructureMap, gitHubStructureMapSchema} from './scenes/GitHubStructureMap';
import {ShellSession, shellSessionSchema} from './scenes/ShellSession';
import {KokoroRosterCard, kokoroRosterCardSchema} from './scenes/KokoroRosterCard';
// claude-medhavy season 1 — "Claude, For Educators"
import {MedhavyConceptCard, medhavyConceptCardSchema} from './scenes/MedhavyConceptCard';
import {MedhavyTwoColumnCard, medhavyTwoColumnCardSchema} from './scenes/MedhavyTwoColumnCard';
import {MedhavyPredictCard, medhavyPredictCardSchema} from './scenes/MedhavyPredictCard';
// claude-musinique season 1 — "Claude, For the Indie"
import {MusiniqueLanes, musiniqueLanesSchema} from './scenes/MusiniqueLanes';
import {MusiniqueSortBranch, musiniqueSortBranchSchema} from './scenes/MusiniqueSortBranch';
import {MusiniqueMismatch, musiniqueMismatchSchema} from './scenes/MusiniqueMismatch';
import {MusiniqueHearingLimit, musiniqueHearingLimitSchema} from './scenes/MusiniqueHearingLimit';
import {MusiniqueArsenal, musiniqueArsenalSchema} from './scenes/MusiniqueArsenal';
// musinique-bookend skill — silent open/close cards for a finished standalone film
import {MusiniqueIntroCard, musiniqueIntroCardSchema, musiniqueIntroCardDefaultProps, MusiniqueIntroCardDemo, musiniqueIntroCardDemoSchema, musiniqueIntroCardDemoDefaultProps} from './scenes/MusiniqueIntroCard';
import {MusiniqueOutroCard, musiniqueOutroCardSchema, musiniqueOutroCardDefaultProps, MusiniqueOutroCardDemo, musiniqueOutroCardDemoSchema, musiniqueOutroCardDemoDefaultProps} from './scenes/MusiniqueOutroCard';
import {ClaudeVerdictArtifact, claudeVerdictArtifactSchema} from './scenes/ClaudeVerdictArtifact';
import {ClaudeVerdictArtifact916, claudeVerdictArtifact916Schema} from './scenes/ClaudeVerdictArtifact916';
import {ClaudeTitleOutro, claudeTitleOutroSchema} from './scenes/ClaudeTitleOutro';
// claude-liam — adaptive-therapy-revolution
import {ClaudeCodeBeat, claudeCodeBeatSchema} from './scenes/ClaudeCodeBeat';
import {ClaudeWindow, claudeWindowSchema} from './scenes/ClaudeWindow';
// claude-liam — 1hr-cowork
import {CoworkHourClock, coworkHourClockSchema} from './scenes/CoworkHourClock';
// Codex interface template library
import {CodexComposerAsk, codexComposerAskSchema} from './scenes/CodexComposerAsk';
import {CodexWindow, codexWindowSchema} from './scenes/CodexWindow';
import {CodexCodeBeat, codexCodeBeatSchema} from './scenes/CodexCodeBeat';
import {CodexCallout, codexCalloutSchema} from './scenes/CodexCallout';
import {CodexTitleOutro, codexTitleOutroSchema} from './scenes/CodexTitleOutro';
// claude-musinique E2 — "Claude, On Schedule"
import {OnScheduleRepurpose, onScheduleRepurposeSchema} from './scenes/OnScheduleRepurpose';
import {OnScheduleDigest, onScheduleDigestSchema} from './scenes/OnScheduleDigest';
import {OnScheduleOvernight, onScheduleOvernightSchema} from './scenes/OnScheduleOvernight';
import {OnScheduleFinePrint, onScheduleFinePrintSchema} from './scenes/OnScheduleFinePrint';
import {OnScheduleRedLine, onScheduleRedLineSchema} from './scenes/OnScheduleRedLine';
// claude-musinique E3 — "Claude, Sourced"
import {SourcedExhibit, sourcedExhibitSchema} from './scenes/SourcedExhibit';
import {SourcedLaundering, sourcedLaunderingSchema} from './scenes/SourcedLaundering';
import {SourcedSorting, sourcedSortingSchema} from './scenes/SourcedSorting';
import {SourcedSkillFile, sourcedSkillFileSchema} from './scenes/SourcedSkillFile';
import {SourcedNoVerdict, sourcedNoVerdictSchema} from './scenes/SourcedNoVerdict';
// claude-musinique E4 — "Claude, In Your Voice"
import {InYourVoiceSkillFile, inYourVoiceSkillFileSchema} from './scenes/InYourVoiceSkillFile';
import {InYourVoiceSpecificity, inYourVoiceSpecificitySchema} from './scenes/InYourVoiceSpecificity';
import {InYourVoiceLyricFile, inYourVoiceLyricFileSchema} from './scenes/InYourVoiceLyricFile';
import {InYourVoicePaper, inYourVoicePaperSchema} from './scenes/InYourVoicePaper';
import {InYourVoiceMoat, inYourVoiceMoatSchema} from './scenes/InYourVoiceMoat';
// claude-musinique E5 — "Claude, On Your Catalog"
import {OnCatalogGrid, onCatalogGridSchema} from './scenes/OnCatalogGrid';
import {OnCatalogHabits, onCatalogHabitsSchema} from './scenes/OnCatalogHabits';
import {OnCatalogThreads, onCatalogThreadsSchema} from './scenes/OnCatalogThreads';
import {OnCatalogReads, onCatalogReadsSchema} from './scenes/OnCatalogReads';
import {OnCatalogData, onCatalogDataSchema} from './scenes/OnCatalogData';
// claude-musinique E6 — "Claude, On the Pitch"
import {OnPitchHomework, onPitchHomeworkSchema} from './scenes/OnPitchHomework';
import {OnPitchDraft, onPitchDraftSchema} from './scenes/OnPitchDraft';
import {OnPitchMountain, onPitchMountainSchema} from './scenes/OnPitchMountain';
import {OnPitchScam, onPitchScamSchema} from './scenes/OnPitchScam';
import {OnPitchVerify, onPitchVerifySchema} from './scenes/OnPitchVerify';
// claude-liam — adaptive-therapy-revolution (full composition)
import {AdaptiveTherapyRevolution, TOTAL_FRAMES as ATR_TOTAL_FRAMES} from './AdaptiveTherapyRevolution';
// ── claude-liam — cancer-biology-all batch retrofit ──
import {CancerDisparitiesZipCode, TOTAL_FRAMES as CancerDisparitiesZipCode_FRAMES} from './CancerDisparitiesZipCode';
import {CancerDormancyRecurrence, TOTAL_FRAMES as CancerDormancyRecurrence_FRAMES} from './CancerDormancyRecurrence';
import {CarTSolidTumorBarrier, TOTAL_FRAMES as CarTSolidTumorBarrier_FRAMES} from './CarTSolidTumorBarrier';
import {ClonalResistancePrediction, TOTAL_FRAMES as ClonalResistancePrediction_FRAMES} from './ClonalResistancePrediction';
import {CtdnaMrdDetection, TOTAL_FRAMES as CtdnaMrdDetection_FRAMES} from './CtdnaMrdDetection';
import {MetastaticCascadeBottleneck, TOTAL_FRAMES as MetastaticCascadeBottleneck_FRAMES} from './MetastaticCascadeBottleneck';
import {NeoantigenaVaccinePipeline, TOTAL_FRAMES as NeoantigenaVaccinePipeline_FRAMES} from './NeoantigenaVaccinePipeline';
import {OncolyticVirotherapy, TOTAL_FRAMES as OncolyticVirotherapy_FRAMES} from './OncolyticVirotherapy';
import {PfsSurrogateEndpoint, TOTAL_FRAMES as PfsSurrogateEndpoint_FRAMES} from './PfsSurrogateEndpoint';
import {PreMetastaticNiche, TOTAL_FRAMES as PreMetastaticNiche_FRAMES} from './PreMetastaticNiche';
import {TumorHeterogeneityTracerx, TOTAL_FRAMES as TumorHeterogeneityTracerx_FRAMES} from './TumorHeterogeneityTracerx';
// ── claude-explainer — cowork-setup ──
import {CoworkSetup, TOTAL_FRAMES as CoworkSetup_FRAMES} from './CoworkSetup';
// ── ruben-substack batch ──
import {ChatgptCopiedClaude, TOTAL_FRAMES as ChatgptCopiedClaude_FRAMES} from './ChatgptCopiedClaude';
import {DontUseClaudeFable5, TOTAL_FRAMES as DontUseClaudeFable5_FRAMES} from './DontUseClaudeFable5';
import {Learn80OfClaudeCoworkIn20Minutes, TOTAL_FRAMES as Learn80OfClaudeCoworkIn20Minutes_FRAMES} from './Learn80OfClaudeCoworkIn20Minutes';
import {WhyAiWillFail, TOTAL_FRAMES as WhyAiWillFail_FRAMES} from './WhyAiWillFail';
import {ClaudeLinkedin, TOTAL_FRAMES as ClaudeLinkedin_FRAMES} from './ClaudeLinkedin';
import {TheClaudeCodeBible, TOTAL_FRAMES as TheClaudeCodeBible_FRAMES} from './TheClaudeCodeBible';
import {IReplacedMyself, TOTAL_FRAMES as IReplacedMyself_FRAMES} from './IReplacedMyself';
import {HowToUseYourPersonalAiAtWork, TOTAL_FRAMES as HowToUseYourPersonalAiAtWork_FRAMES} from './HowToUseYourPersonalAiAtWork';
import {S, TOTAL_FRAMES as S_FRAMES} from './S';
import {ClaudeRoadmap, TOTAL_FRAMES as ClaudeRoadmap_FRAMES} from './ClaudeRoadmap';
import {AiIsASlotMachine, TOTAL_FRAMES as AiIsASlotMachine_FRAMES} from './AiIsASlotMachine';
import {IShookHandsWithANobelPrize, TOTAL_FRAMES as IShookHandsWithANobelPrize_FRAMES} from './IShookHandsWithANobelPrize';
import {HowToMakePerfectSpreadsheets, TOTAL_FRAMES as HowToMakePerfectSpreadsheets_FRAMES} from './HowToMakePerfectSpreadsheets';
import {HowToBeatAiOnceItInevitably, TOTAL_FRAMES as HowToBeatAiOnceItInevitably_FRAMES} from './HowToBeatAiOnceItInevitably';
import {HowToRotYourBrainWithAi, TOTAL_FRAMES as HowToRotYourBrainWithAi_FRAMES} from './HowToRotYourBrainWithAi';
import {ClaudeConnectors, TOTAL_FRAMES as ClaudeConnectors_FRAMES} from './ClaudeConnectors';
import {Prompt47, TOTAL_FRAMES as Prompt47_FRAMES} from './Prompt47';
import {ImClaudeCertified, TOTAL_FRAMES as ImClaudeCertified_FRAMES} from './ImClaudeCertified';
import {YoureJustATextFile, TOTAL_FRAMES as YoureJustATextFile_FRAMES} from './YoureJustATextFile';
import {ItsNotXItsY, TOTAL_FRAMES as ItsNotXItsY_FRAMES} from './ItsNotXItsY';
import {EveryoneWantsOneAi, TOTAL_FRAMES as EveryoneWantsOneAi_FRAMES} from './EveryoneWantsOneAi';
import {ClaudeDesign, TOTAL_FRAMES as ClaudeDesign_FRAMES} from './ClaudeDesign';
import {ClaudeForDummies, TOTAL_FRAMES as ClaudeForDummies_FRAMES} from './ClaudeForDummies';
// claude-musinique E7 — "Claude, In Your Hands"
import {InYourHandsDeck, inYourHandsDeckSchema} from './scenes/InYourHandsDeck';
import {InYourHandsRedLine, inYourHandsRedLineSchema} from './scenes/InYourHandsRedLine';
import {InYourHandsBotVsBot, inYourHandsBotVsBotSchema} from './scenes/InYourHandsBotVsBot';
import {InYourHandsCosts, inYourHandsCostsSchema} from './scenes/InYourHandsCosts';
import {InYourHandsSubscription, inYourHandsSubscriptionSchema} from './scenes/InYourHandsSubscription';

import {LayerStackPreview, SourceFlowPreview, ChipGridPreview, PredictCardPreview} from './illustrations/previews';
// ── claude-liam-claude-science — rhetorical + structural patterns ──
import {AttritionChain, ScaleComparison, BinaryBranch, DivergentFates} from './deckPatterns';
import {
  ClaudeScienceLayerStack, claudeScienceLayerStackSchema,
  ClaudeScienceSourceFlow, claudeScienceSourceFlowSchema,
  ClaudeScienceChipGrid, claudeScienceChipGridSchema,
} from './ClaudeScienceIllu';
// ── claude-liam — math-of-being-afraid-together figures ──
import {HorrorParadox, horrorParadoxSchema} from './scenes/HorrorParadox';
import {HorrorAxiom, horrorAxiomSchema} from './scenes/HorrorAxiom';
import {HorrorComplication, horrorComplicationSchema} from './scenes/HorrorComplication';
import {HorrorEquation, horrorEquationSchema} from './scenes/HorrorEquation';
import {HorrorAlphaHero, horrorAlphaHeroSchema} from './scenes/HorrorAlphaHero';
import {HorrorTriptych, horrorTriptychSchema} from './scenes/HorrorTriptych';
import {HorrorModelBreaks, horrorModelBreaksSchema} from './scenes/HorrorModelBreaks';
import {HorrorProofSpine, horrorProofSpineSchema} from './scenes/HorrorProofSpine';
// ── claude-liam — sleeper-agents figures ──
import {SleeperAgentsBehaviorSwitch, sleeperAgentsBehaviorSwitchSchema} from './scenes/SleeperAgentsBehaviorSwitch';
import {SleeperAgentsBehaviorSwitch916, sleeperAgentsBehaviorSwitch916Schema} from './scenes/SleeperAgentsBehaviorSwitch916';
import {SleeperAgentsExperiment, sleeperAgentsExperimentSchema} from './scenes/SleeperAgentsExperiment';
import {SleeperAgentsExperiment916, sleeperAgentsExperiment916Schema} from './scenes/SleeperAgentsExperiment916';
import {SleeperAgentsResult, sleeperAgentsResultSchema} from './scenes/SleeperAgentsResult';
import {SleeperAgentsResult916, sleeperAgentsResult916Schema} from './scenes/SleeperAgentsResult916';
// ── claude-liam — sycophancy-to-subterfuge figures ──
import {SycGradientSpectrum, sycGradientSpectrumSchema} from './scenes/SycGradientSpectrum';
import {SycCurriculumStages, sycCurriculumStagesSchema} from './scenes/SycCurriculumStages';
import {SycWatcherWatched, sycWatcherWatchedSchema} from './scenes/SycWatcherWatched';
// ── claude-liam — how-we-claude-code figures ──
import {HowWeCode_Phase1, howWeCodePhase1Schema} from './scenes/HowWeCode_Phase1';
import {HowWeCode_Phase2, howWeCodePhase2Schema} from './scenes/HowWeCode_Phase2';
import {HowWeCode_Phase3, howWeCodePhase3Schema} from './scenes/HowWeCode_Phase3';
// ── claude-liam — three-principals figures ──
import {PrincipalsNaiveView, principalsNaiveViewSchema} from './scenes/PrincipalsNaiveView';
import {PrincipalsHierarchy, principalsHierarchySchema} from './scenes/PrincipalsHierarchy';
import {PrincipalsOperatorBounds, principalsOperatorBoundsSchema} from './scenes/PrincipalsOperatorBounds';
// ── claude-liam — ai-skill-formation figures ──
import {AiSkillStudyDesign, aiSkillStudyDesignSchema} from './scenes/AiSkillStudyDesign';
import {AiSkillTreatmentEffect, aiSkillTreatmentEffectSchema} from './scenes/AiSkillTreatmentEffect';
import {AiSkillUsageModes, aiSkillUsageModesSchema} from './scenes/AiSkillUsageModes';
// ── claude-liam — 81k-interviews figures ──
import {WantFig1Scale, wantFig1ScaleSchema} from './scenes/WantFig1Scale';
import {WantFig2Hopes, wantFig2HopesSchema} from './scenes/WantFig2Hopes';
import {WantFig3Delivered, wantFig3DeliveredSchema} from './scenes/WantFig3Delivered';
import {WantFig4Fears, wantFig4FearsSchema} from './scenes/WantFig4Fears';
import {WantFig5LightShade, wantFig5LightShadeSchema} from './scenes/WantFig5LightShade';
import {WantFig6aWorld, wantFig6aWorldSchema} from './scenes/WantFig6aWorld';
import {WantFig6bQuadrant, wantFig6bQuadrantSchema} from './scenes/WantFig6bQuadrant';
import {WantQuote, wantQuoteSchema} from './scenes/WantQuote';
// ── claude-liam — 81k-interviews figures 916 (portrait) ──
import {WantFig1Scale916, wantFig1Scale916Schema} from './scenes/WantFig1Scale916';
import {WantFig2Hopes916, wantFig2Hopes916Schema} from './scenes/WantFig2Hopes916';
import {WantFig3Delivered916, wantFig3Delivered916Schema} from './scenes/WantFig3Delivered916';
import {WantFig4Fears916, wantFig4Fears916Schema} from './scenes/WantFig4Fears916';
import {WantFig6aWorld916, wantFig6aWorld916Schema} from './scenes/WantFig6aWorld916';
import {WantFig6bQuadrant916, wantFig6bQuadrant916Schema} from './scenes/WantFig6bQuadrant916';
import {WantQuote916, wantQuote916Schema} from './scenes/WantQuote916';
// ── claude-liam — claude-values-axes figures ──
import {ValuesCompressionFunnel, valuesCompressionFunnelSchema} from './scenes/ValuesCompressionFunnel';
import {ValuesFourAxes, valuesFourAxesSchema} from './scenes/ValuesFourAxes';
import {ValuesModelProfiles, valuesModelProfilesSchema} from './scenes/ValuesModelProfiles';
import {ValuesLanguageProfiles, valuesLanguageProfilesSchema} from './scenes/ValuesLanguageProfiles';
import {ValuesSplitScreen, valuesSplitScreenSchema} from './scenes/ValuesSplitScreen';
// ── claude-liam — claude-values-axes figures 916 (portrait) ──
import {ValuesCompressionFunnel916, valuesCompressionFunnel916Schema} from './scenes/ValuesCompressionFunnel916';
import {ValuesFourAxes916, valuesFourAxes916Schema} from './scenes/ValuesFourAxes916';
import {ValuesModelProfiles916, valuesModelProfiles916Schema} from './scenes/ValuesModelProfiles916';
import {ValuesSplitScreen916, valuesSplitScreen916Schema} from './scenes/ValuesSplitScreen916';
// ── portrait 916 wrappers for shared components ──
import {ClaudeTitleOutro916, claudeTitleOutro916Schema} from './scenes/ClaudeTitleOutro916';
import {ClaudeWindow916, claudeWindow916Schema} from './scenes/ClaudeWindow916';
// ── claude-liam — coding-agents-social-sciences figures ──
import {CodingAgentsFig1Loop, codingAgentsFig1LoopSchema} from './scenes/CodingAgentsFig1Loop';
import {CodingAgentsFig2Gradient, codingAgentsFig2GradientSchema} from './scenes/CodingAgentsFig2Gradient';
import {CodingAgentsFig3Who, codingAgentsFig3WhoSchema} from './scenes/CodingAgentsFig3Who';
import {CodingAgentsFig4Use, codingAgentsFig4UseSchema} from './scenes/CodingAgentsFig4Use';
import {CodingAgentsFig5Ladder, codingAgentsFig5LadderSchema} from './scenes/CodingAgentsFig5Ladder';
import {CodingAgentsFig6Paradox, codingAgentsFig6ParadoxSchema} from './scenes/CodingAgentsFig6Paradox';
// ── claude-liam — economic-index-cadences figures ──
import {CadencesFig1Clock, cadencesFig1ClockSchema} from './scenes/CadencesFig1Clock';
import {CadencesFig2Tax, cadencesFig2TaxSchema} from './scenes/CadencesFig2Tax';
import {CadencesFig3Artifacts, cadencesFig3ArtifactsSchema} from './scenes/CadencesFig3Artifacts';
import {CadencesFig4Compute, cadencesFig4ComputeSchema} from './scenes/CadencesFig4Compute';
import {CadencesFig5Leash, cadencesFig5LeashSchema} from './scenes/CadencesFig5Leash';
import {CadencesFig6Tide, cadencesFig6TideSchema} from './scenes/CadencesFig6Tide';
import {CadencesFig7Jobs, cadencesFig7JobsSchema} from './scenes/CadencesFig7Jobs';
import {CadencesFig8Paradox, cadencesFig8ParadoxSchema} from './scenes/CadencesFig8Paradox';
import {CadencesFig9Gender, cadencesFig9GenderSchema} from './scenes/CadencesFig9Gender';
import {CadencesFig10Dream, cadencesFig10DreamSchema} from './scenes/CadencesFig10Dream';
// ── claude-liam — teaching-claude-why figures ──
import {TeachClaudeFig1, teachClaudeFig1Schema} from './scenes/TeachClaudeFig1';
import {TeachClaudeFig2, teachClaudeFig2Schema} from './scenes/TeachClaudeFig2';
import {TeachClaudeFig3, teachClaudeFig3Schema} from './scenes/TeachClaudeFig3';
import {TeachClaudeFig4, teachClaudeFig4Schema} from './scenes/TeachClaudeFig4';
import {TeachClaudeFig5, teachClaudeFig5Schema} from './scenes/TeachClaudeFig5';
import {TeachClaudeFig6, teachClaudeFig6Schema} from './scenes/TeachClaudeFig6';
// claude-liam — H logo remotion showcase
import {HLogoRemotionShowcase, TOTAL_FRAMES as HLogoRemotionShowcase_FRAMES} from './HLogoRemotionShowcase';
// claude-liam — H logo remotion showcase (16:9 landscape)
import {HLogoRemotionShowcase169, TOTAL_FRAMES as HLogoRemotionShowcase169_FRAMES} from './HLogoRemotionShowcase169';
// claude-liam — HAI wordmark remotion technique showcase
import {HaiWordmarkShowcase, TOTAL_FRAMES as HaiWordmarkShowcase_FRAMES} from './HaiWordmarkShowcase';
// claude-liam — HAI wordmark remotion technique showcase (16:9 landscape)
import {HaiWordmarkShowcase16x9, TOTAL_FRAMES_16x9 as HaiWordmarkShowcase16x9_FRAMES} from './HaiWordmarkShowcase16x9';
// claude-liam — Musinique logo-2 remotion technique showcase (16:9 landscape)
import {MusiniqueLogo2RemotionShowcase16x9, TOTAL_FRAMES as MusiniqueLogo2Showcase16x9_FRAMES} from './MusiniqueLogo2RemotionShowcase16x9';
// claude-liam — Musinique logo remotion technique showcase (9:16 portrait)
import {MusiniquLogoRemotionShowcase, TOTAL_FRAMES as MusiniquLogoShowcase_FRAMES} from './MusiniquLogoRemotionShowcase';
// claude-liam — Musinique logo-2 remotion technique showcase (9:16 portrait, 20 techniques)
import {MusiniqueLogo2RemotionShowcase, TOTAL_FRAMES as MusiniqueLogo2ShowcasePortrait_FRAMES} from './MusiniqueLogo2RemotionShowcase';
// claude-liam — Bear Brown initials remotion technique showcase (9:16 portrait)
import {BearBrownInitialsShowcase, TOTAL_FRAMES as BearBrownInitialsShowcase_FRAMES} from './BearBrownInitialsShowcase';
// claude-liam — Bear Brown initials remotion technique showcase (16:9 landscape)
import {BearBrownInitialsShowcase169, TOTAL_FRAMES_169 as BearBrownInitialsShowcase169_FRAMES} from './BearBrownInitialsShowcase169';
// claude-liam — Bear Brown full logo remotion technique showcase (9:16 portrait)
import {BearBrownLogoRemotionShowcase, TOTAL_FRAMES as BearBrownLogoShowcase_FRAMES} from './BearBrownLogoRemotionShowcase';
// claude-liam — Bear Brown full logo remotion technique showcase (16:9 landscape)
import {BearBrownLogoRemotionShowcase16x9, TOTAL_FRAMES as BearBrownLogoRemotionShowcase16x9_FRAMES} from './BearBrownLogoRemotionShowcase16x9';
// claude-liam — Musinique logo remotion technique showcase (16:9 landscape, 20 techniques)
import {MusiniquLogoShowcase169, TOTAL_FRAMES_MUSINIQUE} from './MusiniquLogoShowcase169';
// logo skill — the random-once brand sting appended after a reel's last beat
import {LogoOutro, logoOutroSchema} from './scenes/LogoOutro';
import {LogoMotion, logoMotionSchema} from './scenes/LogoMotion';
// ── claude-liam — k12-teacher-skills figures ──
import {K12Fig01Division, k12Fig01DivisionSchema} from './scenes/K12Fig01Division';
import {K12Fig02CRA, k12Fig02CRASchema} from './scenes/K12Fig02CRA';
import {K12Fig03TextScaffold, k12Fig03TextScaffoldSchema} from './scenes/K12Fig03TextScaffold';
import {K12Fig04WorkingMemory, k12Fig04WorkingMemorySchema} from './scenes/K12Fig04WorkingMemory';
import {K12Fig05DiffVsTrack, k12Fig05DiffVsTrackSchema} from './scenes/K12Fig05DiffVsTrack';
import {K12Fig06LoadPartition, k12Fig06LoadPartitionSchema} from './scenes/K12Fig06LoadPartition';
import {K12Fig07ExpertiseReversal, k12Fig07ExpertiseReversalSchema} from './scenes/K12Fig07ExpertiseReversal';
import {K12Fig08ScaffoldContract, k12Fig08ScaffoldContractSchema} from './scenes/K12Fig08ScaffoldContract';
import {K12Fig09ScaffoldVsCrutch, k12Fig09ScaffoldVsCrutchSchema} from './scenes/K12Fig09ScaffoldVsCrutch';
import {K12Fig10FadingSchedule, k12Fig10FadingScheduleSchema} from './scenes/K12Fig10FadingSchedule';
import {K12Fig11SubLedger, k12Fig11SubLedgerSchema} from './scenes/K12Fig11SubLedger';
import {K12Fig12ColdReadTest, k12Fig12ColdReadTestSchema} from './scenes/K12Fig12ColdReadTest';
// ── branding-and-ai — SHOW-DON'T-TELL B01 retrofit figures ──
import {BrandB01SignalCollapse, brandB01SignalCollapseSchema} from './scenes/BrandB01SignalCollapse';
import {BrandB01AlignmentDrift, brandB01AlignmentDriftSchema} from './scenes/BrandB01AlignmentDrift';
import {BrandB01DualTrack, brandB01DualTrackSchema} from './scenes/BrandB01DualTrack';
import {BrandB01ChainFailure, brandB01ChainFailureSchema} from './scenes/BrandB01ChainFailure';
import {BrandB01MonolithGap, brandB01MonolithGapSchema} from './scenes/BrandB01MonolithGap';
import {BrandB01VerbGap, brandB01VerbGapSchema} from './scenes/BrandB01VerbGap';
import {BrandB01DriftTimeline, brandB01DriftTimelineSchema} from './scenes/BrandB01DriftTimeline';
import {BrandB01AttributionConfusion, brandB01AttributionConfusionSchema} from './scenes/BrandB01AttributionConfusion';
import {BrandB01VoiceConflict, brandB01VoiceConflictSchema} from './scenes/BrandB01VoiceConflict';
import {BrandB01RepricingGap, brandB01RepricingGapSchema} from './scenes/BrandB01RepricingGap';
import {BrandB01SeamFailure, brandB01SeamFailureSchema} from './scenes/BrandB01SeamFailure';
import {BrandB01PipelineGap, brandB01PipelineGapSchema} from './scenes/BrandB01PipelineGap';
// ── claude-liam — algorithmic-art figures ──
import {AlgArtPipeline, algArtPipelineSchema} from './scenes/AlgArtPipeline';
import {AlgArtOrganicTurbulence, algArtOrganicTurbulenceSchema} from './scenes/AlgArtOrganicTurbulence';
import {AlgArtMovementGallery, algArtMovementGallerySchema} from './scenes/AlgArtMovementGallery';
import {AlgArtHiddenSeed, algArtHiddenSeedSchema} from './scenes/AlgArtHiddenSeed';
import {AlgArtSeedGrid, algArtSeedGridSchema} from './scenes/AlgArtSeedGrid';
import {AlgArtFixedVariable, algArtFixedVariableSchema} from './scenes/AlgArtFixedVariable';
import {AlgArtQualityDial, algArtQualityDialSchema} from './scenes/AlgArtQualityDial';
// ── claude-liam — agent-development (claude-code) skill teardown figures ──
import {AgentDevAnatomy, agentDevAnatomySchema} from './scenes/AgentDevAnatomy';
import {AgentDevDescription, agentDevDescriptionSchema} from './scenes/AgentDevDescription';
import {AgentDevTell, agentDevTellSchema} from './scenes/AgentDevTell';
// ── claude-liam — xlsx skill teardown figures ──
import {XlsxAnatomy, xlsxAnatomySchema} from './scenes/XlsxAnatomy';
import {XlsxStandards, xlsxStandardsSchema} from './scenes/XlsxStandards';
import {XlsxTell, xlsxTellSchema} from './scenes/XlsxTell';
// ── claude-liam — webapp-testing skill teardown figures ──
import {WebappTestingAnatomy, webappTestingAnatomySchema} from './scenes/WebappTestingAnatomy';
import {WebappTestingPatterns, webappTestingPatternsSchema} from './scenes/WebappTestingPatterns';
import {WebappTestingTell, webappTestingTellSchema} from './scenes/WebappTestingTell';
// ── claude-liam — web-artifacts-builder skill teardown figures ──
import {WebArtifactsAnatomy, webArtifactsAnatomySchema} from './scenes/WebArtifactsAnatomy';
import {WebArtifactsDesign, webArtifactsDesignSchema} from './scenes/WebArtifactsDesign';
import {WebArtifactsTell, webArtifactsTellSchema} from './scenes/WebArtifactsTell';
// ── claude-liam — slack-gif-creator skill teardown figures ──
import {SlackGifAnatomy, slackGifAnatomySchema} from './scenes/SlackGifAnatomy';
import {SlackGifAnimations, slackGifAnimationsSchema} from './scenes/SlackGifAnimations';
import {SlackGifTell, slackGifTellSchema} from './scenes/SlackGifTell';
// ── claude-liam — skill-creator skill teardown figures ──
import {SkillCreatorAnatomy, skillCreatorAnatomySchema} from './scenes/SkillCreatorAnatomy';
import {SkillCreatorEvalLoop, skillCreatorEvalLoopSchema} from './scenes/SkillCreatorEvalLoop';
import {SkillCreatorTell, skillCreatorTellSchema} from './scenes/SkillCreatorTell';
// ── claude-liam — pptx skill teardown figures ──
import {PptxAnatomy, pptxAnatomySchema} from './scenes/PptxAnatomy';
import {PptxDesign, pptxDesignSchema} from './scenes/PptxDesign';
import {PptxTell, pptxTellSchema} from './scenes/PptxTell';
// ── claude-liam — pdf skill teardown figures ──
import {PdfAnatomy, pdfAnatomySchema} from './scenes/PdfAnatomy';
import {PdfOperations, pdfOperationsSchema} from './scenes/PdfOperations';
import {PdfTell, pdfTellSchema} from './scenes/PdfTell';
// ── claude-liam — mcp-builder skill teardown figures ──
import {McpBuilderAnatomy, mcpBuilderAnatomySchema} from './scenes/McpBuilderAnatomy';
import {McpBuilderToolAnatomy, mcpBuilderToolAnatomySchema} from './scenes/McpBuilderToolAnatomy';
import {McpBuilderTell, mcpBuilderTellSchema} from './scenes/McpBuilderTell';
// ── claude-liam — internal-comms skill teardown figures ──
import {InternalCommsAnatomy, internalCommsAnatomySchema} from './scenes/InternalCommsAnatomy';
import {InternalComms3P, internalComms3PSchema} from './scenes/InternalComms3P';
import {InternalCommsTell, internalCommsTellSchema} from './scenes/InternalCommsTell';
// ── claude-liam — frontend-design skill teardown figures ──
import {FrontendDesignAnatomy, frontendDesignAnatomySchema} from './scenes/FrontendDesignAnatomy';
import {FrontendDesignProcess, frontendDesignProcessSchema} from './scenes/FrontendDesignProcess';
import {FrontendDesignRestraint, frontendDesignRestraintSchema} from './scenes/FrontendDesignRestraint';
import {FrontendDesignTell, frontendDesignTellSchema} from './scenes/FrontendDesignTell';
// ── claude-liam — docx skill teardown figures ──
import {DocxAnatomy, docxAnatomySchema} from './scenes/DocxAnatomy';
import {DocxCreate, docxCreateSchema} from './scenes/DocxCreate';
import {DocxEdit, docxEditSchema} from './scenes/DocxEdit';
import {DocxTell, docxTellSchema} from './scenes/DocxTell';
// ── claude-liam — doc-coauthoring skill teardown figures ──
import {DocCoauthoringAnatomy, docCoauthoringAnatomySchema} from './scenes/DocCoauthoringAnatomy';
import {DocCoauthoringStage1, docCoauthoringStage1Schema} from './scenes/DocCoauthoringStage1';
import {DocCoauthoringStage2, docCoauthoringStage2Schema} from './scenes/DocCoauthoringStage2';
import {DocCoauthoringStage3, docCoauthoringStage3Schema} from './scenes/DocCoauthoringStage3';
import {DocCoauthoringTell, docCoauthoringTellSchema} from './scenes/DocCoauthoringTell';
// ── claude-liam — claude-api skill teardown figures ──
import {ClaudeApiAnatomy, claudeApiAnatomySchema} from './scenes/ClaudeApiAnatomy';
import {ClaudeApiSurfaces, claudeApiSurfacesSchema} from './scenes/ClaudeApiSurfaces';
import {ClaudeApiDrift, claudeApiDriftSchema} from './scenes/ClaudeApiDrift';
import {ClaudeApiModels, claudeApiModelsSchema} from './scenes/ClaudeApiModels';
import {ClaudeApiTell, claudeApiTellSchema} from './scenes/ClaudeApiTell';
// ── claude-liam — canvas-design skill teardown figures ──
import {CanvasDesignAnatomy, canvasDesignAnatomySchema} from './scenes/CanvasDesignAnatomy';
import {CanvasDesignPipeline, canvasDesignPipelineSchema} from './scenes/CanvasDesignPipeline';
import {CanvasDesignPhilosophy, canvasDesignPhilosophySchema} from './scenes/CanvasDesignPhilosophy';
import {CanvasDesignCanvas, canvasDesignCanvasSchema} from './scenes/CanvasDesignCanvas';
import {CanvasDesignTell, canvasDesignTellSchema} from './scenes/CanvasDesignTell';
// ── claude-liam — brand-guidelines skill teardown figures ──
import {BrandGuidelinesAnatomy, brandGuidelinesAnatomySchema} from './scenes/BrandGuidelinesAnatomy';
import {BrandGuidelinesPipeline, brandGuidelinesPipelineSchema} from './scenes/BrandGuidelinesPipeline';
import {BrandGuidelinesPalette, brandGuidelinesPaletteSchema} from './scenes/BrandGuidelinesPalette';
import {BrandGuidelinesTypography, brandGuidelinesTypographySchema} from './scenes/BrandGuidelinesTypography';
import {BrandGuidelinesDesignTell, brandGuidelinesDesignTellSchema} from './scenes/BrandGuidelinesDesignTell';
// ── claude-liam — theme-factory figures ──
import {ThemeFactoryAnatomy, themeFactoryAnatomySchema} from './scenes/ThemeFactoryAnatomy';
import {ThemeFactoryThemeCard, themeFactoryThemeCardSchema} from './scenes/ThemeFactoryThemeCard';
import {ThemeFactoryConsentGate, themeFactoryConsentGateSchema} from './scenes/ThemeFactoryConsentGate';
import {ThemeFactoryTenSkins, themeFactoryTenSkinsSchema} from './scenes/ThemeFactoryTenSkins';
import {ThemeFactoryMirror, themeFactoryMirrorSchema} from './scenes/ThemeFactoryMirror';
import {ThemeFactoryCustomTheme, themeFactoryCustomThemeSchema} from './scenes/ThemeFactoryCustomTheme';
import {ThemeFactoryContrastMeter, themeFactoryContrastMeterSchema} from './scenes/ThemeFactoryContrastMeter';
// ── cwc-workshops — Code with Claude 2026 batch figures ──
import {CwcMemoryTimeline, cwcMemoryTimelineSchema} from './scenes/CwcMemoryTimeline';
import {CwcSixVariants, cwcSixVariantsSchema} from './scenes/CwcSixVariants';
import {CwcFanOutFlow, cwcFanOutFlowSchema} from './scenes/CwcFanOutFlow';
import {CwcDecompositionTree, cwcDecompositionTreeSchema} from './scenes/CwcDecompositionTree';
import {CwcParetoScatter, cwcParetoScatterSchema} from './scenes/CwcParetoScatter';
// ── cwc-workshops — expanded deep-dive scenes ──
import {CwcSkillCallMechanism, cwcSkillCallMechanismSchema} from './scenes/CwcSkillCallMechanism';
import {CwcToolVsSkillComparison, cwcToolVsSkillComparisonSchema} from './scenes/CwcToolVsSkillComparison';
import {CwcCostLatencyGain, cwcCostLatencyGainSchema} from './scenes/CwcCostLatencyGain';
import {CwcMemorySchema, cwcMemorySchemaSchema} from './scenes/CwcMemorySchema';
import {CwcDreamingService, cwcDreamingServiceSchema} from './scenes/CwcDreamingService';
import {CwcMemoryRetrieval, cwcMemoryRetrievalSchema} from './scenes/CwcMemoryRetrieval';
import {CwcFanOutSpeedGain, cwcFanOutSpeedGainSchema} from './scenes/CwcFanOutSpeedGain';
import {CwcResultAggregation, cwcResultAggregationSchema} from './scenes/CwcResultAggregation';
import {CwcOrchestrationContract, cwcOrchestrationContractSchema} from './scenes/CwcOrchestrationContract';
import {CwcEvalScoring, cwcEvalScoringSchema} from './scenes/CwcEvalScoring';
import {CwcVariantImprovementWaterfall, cwcVariantImprovementWaterfallSchema} from './scenes/CwcVariantImprovementWaterfall';
import {CwcWhenToEval, cwcWhenToEvalSchema} from './scenes/CwcWhenToEval';
import {CwcModelCostComparison, cwcModelCostComparisonSchema} from './scenes/CwcModelCostComparison';
import {CwcFrontierSelection, cwcFrontierSelectionSchema} from './scenes/CwcFrontierSelection';
import {CwcSweepInPractice, cwcSweepInPracticeSchema} from './scenes/CwcSweepInPractice';
// ── claude-liam — profile: Kaustubha Venkata Eluri ──
import {ProfileKaustubhaFig1Gap, profileKaustubhaFig1GapSchema} from './scenes/ProfileKaustubhaFig1Gap';
import {ProfileKaustubhaFig2ModelSystem, profileKaustubhaFig2ModelSystemSchema} from './scenes/ProfileKaustubhaFig2ModelSystem';
import {ProfileKaustubhaFig3Projects, profileKaustubhaFig3ProjectsSchema} from './scenes/ProfileKaustubhaFig3Projects';
import {ProfileKaustubhaFig4Resilience, profileKaustubhaFig4ResilienceSchema} from './scenes/ProfileKaustubhaFig4Resilience';
import {ProfileKaustubhaFig5CitedUsed, profileKaustubhaFig5CitedUsedSchema} from './scenes/ProfileKaustubhaFig5CitedUsed';
import {ProfileKaustubhaCredit, profileKaustubhaCreditSchema} from './scenes/ProfileKaustubhaCredit';
// ── claude-liam — profile: Aditi Deodhar ──
import {ProfileAditiFig1Pivot, profileAditiFig1PivotSchema} from './scenes/ProfileAditiFig1Pivot';
import {ProfileAditiFig2Stack, profileAditiFig2StackSchema} from './scenes/ProfileAditiFig2Stack';
import {ProfileAditiFig3Builds, profileAditiFig3BuildsSchema} from './scenes/ProfileAditiFig3Builds';
import {ProfileAditiFig4Community, profileAditiFig4CommunitySchema} from './scenes/ProfileAditiFig4Community';
import {ProfileAditiFig5Record, profileAditiFig5RecordSchema} from './scenes/ProfileAditiFig5Record';
import {ProfileAditiFig6Quote, profileAditiFig6QuoteSchema} from './scenes/ProfileAditiFig6Quote';
import {ProfileAditiCredit, profileAditiCreditSchema} from './scenes/ProfileAditiCredit';
// ── claude-liam-hai — how-to-explainer-videos figures ──
import {HaiExplainerFig1Pipeline, haiExplainerFig1PipelineSchema} from './scenes/HaiExplainerFig1Pipeline';
import {HaiExplainerFig2Folder, haiExplainerFig2FolderSchema} from './scenes/HaiExplainerFig2Folder';
import {HaiExplainerFig3Command, haiExplainerFig3CommandSchema} from './scenes/HaiExplainerFig3Command';
import {HaiExplainerFig4Prompt, haiExplainerFig4PromptSchema} from './scenes/HaiExplainerFig4Prompt';
import {HaiExplainerFig5Revise, haiExplainerFig5ReviseSchema} from './scenes/HaiExplainerFig5Revise';
import {HaiExplainerFig6Publish, haiExplainerFig6PublishSchema} from './scenes/HaiExplainerFig6Publish';
// ── HAI Brutalist Fellows Series E01–E12 ──
import {HaiBrutalistE01Pipeline, haiBrutalistE01PipelineSchema} from './scenes/HaiBrutalistE01Pipeline';
import {HaiBrutalistE02Reach, haiBrutalistE02ReachSchema} from './scenes/HaiBrutalistE02Reach';
import {HaiBrutalistE03Install, haiBrutalistE03InstallSchema} from './scenes/HaiBrutalistE03Install';
import {HaiBrutalistE04Folder, haiBrutalistE04FolderSchema} from './scenes/HaiBrutalistE04Folder';
import {HaiBrutalistE05Command, haiBrutalistE05CommandSchema} from './scenes/HaiBrutalistE05Command';
import {HaiBrutalistE07BeatSheet, haiBrutalistE07BeatSheetSchema} from './scenes/HaiBrutalistE07BeatSheet';
import {HaiBrutalistE08Voices, haiBrutalistE08VoicesSchema} from './scenes/HaiBrutalistE08Voices';
import {HaiBrutalistE09Rebuild, haiBrutalistE09RebuildSchema} from './scenes/HaiBrutalistE09Rebuild';
import {HaiBrutalistE10Revise, haiBrutalistE10ReviseSchema} from './scenes/HaiBrutalistE10Revise';
import {HaiBrutalistE11Publish, haiBrutalistE11PublishSchema} from './scenes/HaiBrutalistE11Publish';
import {HaiBrutalistE12Profile, haiBrutalistE12ProfileSchema} from './scenes/HaiBrutalistE12Profile';
// ── branding-and-ai — Nina Harris course batch (C01–C12) ──
import {BrandSignalMatrix, brandSignalMatrixSchema} from './scenes/BrandSignalMatrix';
import {BrandArchetypeWheel, brandArchetypeWheelSchema} from './scenes/BrandArchetypeWheel';
import {BrandMetricsTimeline, brandMetricsTimelineSchema} from './scenes/BrandMetricsTimeline';
import {BrandPipelineAudit, brandPipelineAuditSchema} from './scenes/BrandPipelineAudit';
import {BrandAgentMapper, brandAgentMapperSchema} from './scenes/BrandAgentMapper';
import {BrandVerbScorecard, brandVerbScorecardSchema} from './scenes/BrandVerbScorecard';
import {BrandDriftCaseStudy, brandDriftCaseStudySchema} from './scenes/BrandDriftCaseStudy';
import {BrandAttributionCheck, brandAttributionCheckSchema} from './scenes/BrandAttributionCheck';
import {BrandVoiceAudit, brandVoiceAuditSchema} from './scenes/BrandVoiceAudit';
import {BrandRepricingTable, brandRepricingTableSchema} from './scenes/BrandRepricingTable';
import {BrandBoondoggleScore, brandBoondoggleScoreSchema} from './scenes/BrandBoondoggleScore';
import {BrandSelfPipeline, brandSelfPipelineSchema} from './scenes/BrandSelfPipeline';
// ── claude-liam — vercel-mcp figures ──
import {VercelOfficial, vercelOfficialSchema} from './scenes/VercelOfficial';
import {VercelDiagnose, vercelDiagnoseSchema} from './scenes/VercelDiagnose';
import {VercelAccountEquivalent, vercelAccountEquivalentSchema} from './scenes/VercelAccountEquivalent';
import {VercelBuyDomain, vercelBuyDomainSchema} from './scenes/VercelBuyDomain';
import {VercelSafeguardGap, vercelSafeguardGapSchema} from './scenes/VercelSafeguardGap';
import {VercelOwnGuidance, vercelOwnGuidanceSchema} from './scenes/VercelOwnGuidance';
import {VercelMitigations, vercelMitigationsSchema} from './scenes/VercelMitigations';
// ── claude-liam-a5a — "Wrap It & Test It" series figures ──
import {A5aFrameworkChoice, a5aFrameworkChoiceSchema} from './scenes/A5aFrameworkChoice';
import {A5aInputWiring, a5aInputWiringSchema} from './scenes/A5aInputWiring';
import {A5aOutputFormat, a5aOutputFormatSchema} from './scenes/A5aOutputFormat';
// ── claude-liam-a8 — "Ship It" series figures ──
import {A8DeliverableMap, a8DeliverableMapSchema} from './scenes/A8DeliverableMap';
import {A8ShipItRule, a8ShipItRuleSchema} from './scenes/A8ShipItRule';
// ── claude-liam — connect-linkedin figures ──
import {LinkedInTrustBoundary, linkedInTrustBoundarySchema} from './scenes/LinkedInTrustBoundary';
import {LinkedInThreeLanes, linkedInThreeLanesSchema} from './scenes/LinkedInThreeLanes';
import {LinkedInAsymmetry, linkedInAsymmetrySchema} from './scenes/LinkedInAsymmetry';
import {LinkedInApiSurface, linkedInApiSurfaceSchema} from './scenes/LinkedInApiSurface';
import {LinkedInDetectionStack, linkedInDetectionStackSchema} from './scenes/LinkedInDetectionStack';
import {LinkedInLegalSplit, linkedInLegalSplitSchema} from './scenes/LinkedInLegalSplit';
import {LinkedInRedFlags, linkedInRedFlagsSchema} from './scenes/LinkedInRedFlags';

import {
  CwcExclusions, cwcExclusionsSchema,
  CwcConceptCard, cwcConceptCardSchema,
  CwcMemoryQuestion, cwcMemoryQuestionSchema,
  CwcSessionIsolation, cwcSessionIsolationSchema,
  CwcMemoryProgression, cwcMemoryProgressionSchema,
  CwcEvalQuestion, cwcEvalQuestionSchema,
  CwcTwoLayerEval, cwcTwoLayerEvalSchema,
  CwcVariantAccumulation, cwcVariantAccumulationSchema,
  CwcOrchestrationQuestion, cwcOrchestrationQuestionSchema,
  CwcFanOutConcept, cwcFanOutConceptSchema,
  CwcSpreadMechanism, cwcSpreadMechanismSchema,
  CwcDecompositionQuestion, cwcDecompositionQuestionSchema,
  CwcThreeLevers, cwcThreeLeversSchema,
  CwcSplitMechanism, cwcSplitMechanismSchema,
  CwcModelQuestion, cwcModelQuestionSchema,
  CwcParetoExplained, cwcParetoExplainedSchema,
  CwcSweepAccumulation, cwcSweepAccumulationSchema,
} from './scenes/CwcShared';
// ── claude-liam — sentry-api (claude-tag-plugins) skill teardown figures ──
import {SentryApiAnatomy, sentryApiAnatomySchema} from './scenes/SentryApiAnatomy';
import {SentryApiDesign, sentryApiDesignSchema} from './scenes/SentryApiDesign';
import {SentryApiTell, sentryApiTellSchema} from './scenes/SentryApiTell';
// ── claude-liam — salesforce-api (claude-tag-plugins) skill teardown figures ──
import {SalesforceApiAnatomy, salesforceApiAnatomySchema} from './scenes/SalesforceApiAnatomy';
import {SalesforceApiDesign, salesforceApiDesignSchema} from './scenes/SalesforceApiDesign';
import {SalesforceApiTell, salesforceApiTellSchema} from './scenes/SalesforceApiTell';
// ── claude-liam — redshift-api (claude-tag-plugins) skill teardown figures ──
import {RedshiftApiAnatomy, redshiftApiAnatomySchema} from './scenes/RedshiftApiAnatomy';
import {RedshiftApiDesign, redshiftApiDesignSchema} from './scenes/RedshiftApiDesign';
import {RedshiftApiTell, redshiftApiTellSchema} from './scenes/RedshiftApiTell';
// ── claude-liam — project-artifact (claude-plugins-official) skill teardown figures ──
import {ProjectArtifactAnatomy, projectArtifactAnatomySchema} from './scenes/ProjectArtifactAnatomy';
import {ProjectArtifactDesign, projectArtifactDesignSchema} from './scenes/ProjectArtifactDesign';
import {ProjectArtifactTell, projectArtifactTellSchema} from './scenes/ProjectArtifactTell';
// ── claude-liam — playground (claude-plugins-official) skill teardown figures ──
import {PlaygroundAnatomy, playgroundAnatomySchema} from './scenes/PlaygroundAnatomy';
import {PlaygroundDesign, playgroundDesignSchema} from './scenes/PlaygroundDesign';
import {PlaygroundTell, playgroundTellSchema} from './scenes/PlaygroundTell';
// ── claude-liam — pagerduty-api (claude-tag-plugins) skill teardown figures ──
import {PagerdutyApiAnatomy, pagerdutyApiAnatomySchema} from './scenes/PagerdutyApiAnatomy';
import {PagerdutyApiDesign, pagerdutyApiDesignSchema} from './scenes/PagerdutyApiDesign';
import {PagerdutyApiTell, pagerdutyApiTellSchema} from './scenes/PagerdutyApiTell';
// ── claude-liam — notion-api (claude-tag-plugins) skill teardown figures ──
import {NotionApiAnatomy, notionApiAnatomySchema} from './scenes/NotionApiAnatomy';
import {NotionApiDesign, notionApiDesignSchema} from './scenes/NotionApiDesign';
import {NotionApiTell, notionApiTellSchema} from './scenes/NotionApiTell';
// ── claude-liam — mcp-integration (claude-plugins-official) skill teardown figures ──
import {McpIntegrationAnatomy, mcpIntegrationAnatomySchema} from './scenes/McpIntegrationAnatomy';
import {McpIntegrationDesign, mcpIntegrationDesignSchema} from './scenes/McpIntegrationDesign';
import {McpIntegrationTell, mcpIntegrationTellSchema} from './scenes/McpIntegrationTell';
// ── claude-liam — math-olympiad (claude-plugins-official) skill teardown figures ──
import {MathOlympiadAnatomy, mathOlympiadAnatomySchema} from './scenes/MathOlympiadAnatomy';
import {MathOlympiadDesign, mathOlympiadDesignSchema} from './scenes/MathOlympiadDesign';
import {MathOlympiadTell, mathOlympiadTellSchema} from './scenes/MathOlympiadTell';
// ── claude-liam — m5-onboard (claude-plugins-official) skill teardown figures ──
import {M5OnboardAnatomy, m5OnboardAnatomySchema} from './scenes/M5OnboardAnatomy';
import {M5OnboardDesign, m5OnboardDesignSchema} from './scenes/M5OnboardDesign';
import {M5OnboardTell, m5OnboardTellSchema} from './scenes/M5OnboardTell';
// ── claude-liam — linear-api (claude-tag-plugins) skill teardown figures ──
import {LinearApiAnatomy, linearApiAnatomySchema} from './scenes/LinearApiAnatomy';
import {LinearApiDesign, linearApiDesignSchema} from './scenes/LinearApiDesign';
import {LinearApiTell, linearApiTellSchema} from './scenes/LinearApiTell';
// ── claude-liam — jira-api (claude-tag-plugins) skill teardown figures ──
import {JiraApiAnatomy, jiraApiAnatomySchema} from './scenes/JiraApiAnatomy';
import {JiraApiDesign, jiraApiDesignSchema} from './scenes/JiraApiDesign';
import {JiraApiTell, jiraApiTellSchema} from './scenes/JiraApiTell';
// ── claude-liam — hubspot-api (claude-tag-plugins) skill teardown figures ──
import {HubSpotApiAnatomy, hubSpotApiAnatomySchema} from './scenes/HubSpotApiAnatomy';
import {HubSpotApiDesign, hubSpotApiDesignSchema} from './scenes/HubSpotApiDesign';
import {HubSpotApiTell, hubSpotApiTellSchema} from './scenes/HubSpotApiTell';
// ── claude-liam — hook-development (claude-plugins-official) skill teardown figures ──
import {HookDevelopmentAnatomy, hookDevelopmentAnatomySchema} from './scenes/HookDevelopmentAnatomy';
import {HookDevelopmentDesign, hookDevelopmentDesignSchema} from './scenes/HookDevelopmentDesign';
import {HookDevelopmentTell, hookDevelopmentTellSchema} from './scenes/HookDevelopmentTell';
// ── claude-liam — graphing (claude-tag-plugins) skill teardown figures ──
import {GraphingAnatomy, graphingAnatomySchema} from './scenes/GraphingAnatomy';
import {GraphingDesign, graphingDesignSchema} from './scenes/GraphingDesign';
import {GraphingTell, graphingTellSchema} from './scenes/GraphingTell';
// ── claude-liam — grafana-api (claude-tag-plugins) skill teardown figures ──
import {GrafanaApiAnatomy, grafanaApiAnatomySchema} from './scenes/GrafanaApiAnatomy';
import {GrafanaApiDesign, grafanaApiDesignSchema} from './scenes/GrafanaApiDesign';
import {GrafanaApiTell, grafanaApiTellSchema} from './scenes/GrafanaApiTell';
// ── claude-liam — google-drive-api (claude-tag-plugins) skill teardown figures ──
import {GoogleDriveApiAnatomy, googleDriveApiAnatomySchema} from './scenes/GoogleDriveApiAnatomy';
import {GoogleDriveApiDesign, googleDriveApiDesignSchema} from './scenes/GoogleDriveApiDesign';
import {GoogleDriveApiTell, googleDriveApiTellSchema} from './scenes/GoogleDriveApiTell';
// ── claude-liam — example-skill (claude-plugins-official) skill teardown figures ──
import {ExampleSkillAnatomy, exampleSkillAnatomySchema} from './scenes/ExampleSkillAnatomy';
import {ExampleSkillDesign, exampleSkillDesignSchema} from './scenes/ExampleSkillDesign';
import {ExampleSkillTell, exampleSkillTellSchema} from './scenes/ExampleSkillTell';
// ── claude-liam — example-command (claude-plugins-official) skill teardown figures ──
import {ExampleCommandAnatomy, exampleCommandAnatomySchema} from './scenes/ExampleCommandAnatomy';
import {ExampleCommandDesign, exampleCommandDesignSchema} from './scenes/ExampleCommandDesign';
import {ExampleCommandTell, exampleCommandTellSchema} from './scenes/ExampleCommandTell';
// ── claude-liam — enterprise-search (claude-tag-plugins) skill teardown figures ──
import {EnterpriseSearchAnatomy, enterpriseSearchAnatomySchema} from './scenes/EnterpriseSearchAnatomy';
import {EnterpriseSearchDesign, enterpriseSearchDesignSchema} from './scenes/EnterpriseSearchDesign';
import {EnterpriseSearchTell, enterpriseSearchTellSchema} from './scenes/EnterpriseSearchTell';
// ── claude-liam — debug-plugins (claude-tag-plugins) skill teardown figures ──
import {DebugPluginsAnatomy, debugPluginsAnatomySchema} from './scenes/DebugPluginsAnatomy';
import {DebugPluginsDesign, debugPluginsDesignSchema} from './scenes/DebugPluginsDesign';
import {DebugPluginsTell, debugPluginsTellSchema} from './scenes/DebugPluginsTell';
// ── claude-liam — datadog-api (claude-tag-plugins) skill teardown figures ──
import {DatadogApiAnatomy, datadogApiAnatomySchema} from './scenes/DatadogApiAnatomy';
import {DatadogApiDesign, datadogApiDesignSchema} from './scenes/DatadogApiDesign';
import {DatadogApiTell, datadogApiTellSchema} from './scenes/DatadogApiTell';
// ── claude-liam — confluence-api (claude-tag-plugins) skill teardown figures ──
import {ConfluenceApiAnatomy, confluenceApiAnatomySchema} from './scenes/ConfluenceApiAnatomy';
import {ConfluenceApiDesign, confluenceApiDesignSchema} from './scenes/ConfluenceApiDesign';
import {ConfluenceApiTell, confluenceApiTellSchema} from './scenes/ConfluenceApiTell';
// ── claude-liam — configure (claude-plugins-official discord) skill teardown figures ──
import {ConfigureAnatomy, configureAnatomySchema} from './scenes/ConfigureAnatomy';
import {ConfigureDesign, configureDesignSchema} from './scenes/ConfigureDesign';
import {ConfigureTell, configureTellSchema} from './scenes/ConfigureTell';
// ── claude-liam — config-guide (claude-tag-plugins) skill teardown figures ──
import {ConfigGuideAnatomy, configGuideAnatomySchema} from './scenes/ConfigGuideAnatomy';
import {ConfigGuideDesign, configGuideDesignSchema} from './scenes/ConfigGuideDesign';
import {ConfigGuideTell, configGuideTellSchema} from './scenes/ConfigGuideTell';
// ── claude-liam — claude-opus-4-5-migration (claude-code) skill teardown figures ──
import {Opus45MigrationMatrix, opus45MigrationMatrixSchema} from './scenes/Opus45MigrationMatrix';
import {Opus45MigrationTriggers, opus45MigrationTriggersSchema} from './scenes/Opus45MigrationTriggers';
import {Opus45MigrationTell, opus45MigrationTellSchema} from './scenes/Opus45MigrationTell';
// ── claude-liam — claude-md-improver (claude-plugins-official) skill teardown figures ──
import {ClaudeMdImproverLocations, claudeMdImproverLocationsSchema} from './scenes/ClaudeMdImproverLocations';
import {ClaudeMdImproverWorkflow, claudeMdImproverWorkflowSchema} from './scenes/ClaudeMdImproverWorkflow';
import {ClaudeMdImproverTell, claudeMdImproverTellSchema} from './scenes/ClaudeMdImproverTell';
// ── claude-liam — claude-automation-recommender (claude-plugins-official) skill teardown figures ──
import {AutomationRecommenderTypes, automationRecommenderTypesSchema} from './scenes/AutomationRecommenderTypes';
import {AutomationRecommenderSignals, automationRecommenderSignalsSchema} from './scenes/AutomationRecommenderSignals';
import {AutomationRecommenderTell, automationRecommenderTellSchema} from './scenes/AutomationRecommenderTell';
// ── claude-liam — cardputer-buddy (claude-plugins-official) skill teardown figures ──
import {CardputerBuddyLayout, cardputerBuddyLayoutSchema} from './scenes/CardputerBuddyLayout';
import {CardputerBuddyScripts, cardputerBuddyScriptsSchema} from './scenes/CardputerBuddyScripts';
import {CardputerBuddyTell, cardputerBuddyTellSchema} from './scenes/CardputerBuddyTell';
// ── claude-liam — build-mcpb (claude-plugins-official) skill teardown figures ──
import {BuildMcpbAnatomy, buildMcpbAnatomySchema} from './scenes/BuildMcpbAnatomy';
import {BuildMcpbPipeline, buildMcpbPipelineSchema} from './scenes/BuildMcpbPipeline';
import {BuildMcpbTell, buildMcpbTellSchema} from './scenes/BuildMcpbTell';
// ── claude-liam — build-mcp-server (claude-plugins-official) skill teardown figures ──
import {BuildMcpServerDeployment, buildMcpServerDeploymentSchema} from './scenes/BuildMcpServerDeployment';
import {BuildMcpServerPatterns, buildMcpServerPatternsSchema} from './scenes/BuildMcpServerPatterns';
import {BuildMcpServerTell, buildMcpServerTellSchema} from './scenes/BuildMcpServerTell';
// ── claude-liam — build-mcp-app (claude-plugins-official) skill teardown figures ──
import {BuildMcpAppAnatomy, buildMcpAppAnatomySchema} from './scenes/BuildMcpAppAnatomy';
import {BuildMcpAppDecision, buildMcpAppDecisionSchema} from './scenes/BuildMcpAppDecision';
import {BuildMcpAppTell, buildMcpAppTellSchema} from './scenes/BuildMcpAppTell';
// ── claude-liam — bigquery-api (claude-tag-plugins) skill teardown figures ──
import {BigQueryApiAnatomy, bigQueryApiAnatomySchema} from './scenes/BigQueryApiAnatomy';
import {BigQueryApiOps, bigQueryApiOpsSchema} from './scenes/BigQueryApiOps';
import {BigQueryApiTell, bigQueryApiTellSchema} from './scenes/BigQueryApiTell';
// ── claude-liam — asana-api (claude-tag-plugins) skill teardown figures ──
import {AsanaApiAnatomy, asanaApiAnatomySchema} from './scenes/AsanaApiAnatomy';
import {AsanaApiOps, asanaApiOpsSchema} from './scenes/AsanaApiOps';
import {AsanaApiTell, asanaApiTellSchema} from './scenes/AsanaApiTell';
// ── claude-liam — agent-development (claude-plugins-official) prose-trigger figures ──
import {AgentDevTriggerProse, agentDevTriggerProseSchema} from './scenes/AgentDevTriggerProse';
import {AgentDevTell2, agentDevTell2Schema} from './scenes/AgentDevTell2';
// ── claude-liam — access (discord plugin) skill teardown figures ──
import {DiscordAccessAnatomy, discordAccessAnatomySchema} from './scenes/DiscordAccessAnatomy';
import {DiscordAccessCommands, discordAccessCommandsSchema} from './scenes/DiscordAccessCommands';
import {DiscordAccessTell, discordAccessTellSchema} from './scenes/DiscordAccessTell';
// ── claude-liam — writing-rules (hookify plugin) skill teardown figures ──
import {HookifyRuleAnatomy, hookifyRuleAnatomySchema} from './scenes/HookifyRuleAnatomy';
import {HookifyEventTypes, hookifyEventTypesSchema} from './scenes/HookifyEventTypes';
import {HookifyTell, hookifyTellSchema} from './scenes/HookifyTell';
// ── claude-liam — skill-development (claude-code) skill teardown figures ──
import {SkillDevAnatomy, skillDevAnatomySchema} from './scenes/SkillDevAnatomy';
import {SkillDevProcess, skillDevProcessSchema} from './scenes/SkillDevProcess';
import {SkillDevTell, skillDevTellSchema} from './scenes/SkillDevTell';
// ── claude-liam — plugin-structure (claude-code) skill teardown figures ──
import {PluginStructureAnatomy, pluginStructureAnatomySchema} from './scenes/PluginStructureAnatomy';
import {PluginStructureComponents, pluginStructureComponentsSchema} from './scenes/PluginStructureComponents';
import {PluginStructureTell, pluginStructureTellSchema} from './scenes/PluginStructureTell';
// ── claude-liam — plugin-settings (claude-code) skill teardown figures ──
import {PluginSettingsAnatomy, pluginSettingsAnatomySchema} from './scenes/PluginSettingsAnatomy';
import {PluginSettingsPatterns, pluginSettingsPatternsSchema} from './scenes/PluginSettingsPatterns';
import {PluginSettingsTell, pluginSettingsTellSchema} from './scenes/PluginSettingsTell';
// ── claude-liam — mcp-integration (claude-code) skill teardown figures ──
import {McpIntAnatomy, mcpIntAnatomySchema} from './scenes/McpIntAnatomy';
import {McpIntPatterns, mcpIntPatternsSchema} from './scenes/McpIntPatterns';
import {McpIntTell, mcpIntTellSchema} from './scenes/McpIntTell';
// ── claude-liam — hook-development (claude-code) skill teardown figures ──
import {HookDevAnatomy, hookDevAnatomySchema} from './scenes/HookDevAnatomy';
import {HookDevConfig, hookDevConfigSchema} from './scenes/HookDevConfig';
import {HookDevTell, hookDevTellSchema} from './scenes/HookDevTell';
// ── claude-liam — command-development (claude-code) skill teardown figures ──
import {CommandDevAnatomy, commandDevAnatomySchema} from './scenes/CommandDevAnatomy';
import {CommandDevContent, commandDevContentSchema} from './scenes/CommandDevContent';
import {CommandDevTell, commandDevTellSchema} from './scenes/CommandDevTell';
// ── generic skill-teardown templates (meta-series batch) ──
import {SkillTeardownAnatomy, skillTeardownAnatomySchema} from './scenes/SkillTeardownAnatomy';
import {SkillTeardownPipeline, skillTeardownPipelineSchema} from './scenes/SkillTeardownPipeline';
import {SkillTeardownMechanism, skillTeardownMechanismSchema} from './scenes/SkillTeardownMechanism';
// ── claude-liam-fluency-trap — reel-local components ──
import {
  FluencySegmentCard, fluencySegmentCardSchema,
  FluencyDivergence,  fluencyDivergenceSchema,
  FluencyThreshold,   fluencyThresholdSchema,
  FluencySourceFlow,  fluencySourceFlowSchema,
  FluencyScale,       fluencyScaleSchema,
  FluencyVerdictStamps, fluencyVerdictStampsSchema,
  FluencyChipGrid,    fluencyChipGridSchema,
} from './FluencyTrap';
// ── claude-liam-what-a-university-can-require — reel-local components ──
import {
  ReqSegmentCard,    reqSegmentCardSchema,
  ReqBars,           reqBarsSchema,
  ReqLedger,         reqLedgerSchema,
  ReqDefinitionDrop, reqDefinitionDropSchema,
  ReqLevers,         reqLeversSchema,
  ReqRingWord,       reqRingWordSchema,
} from './RequireReport';
// ── claude-liam-train-the-teacher ── reel-local components ──
import {
  TtTwoAnswers,   ttTwoAnswersSchema,
  TtFrontLoaded,  ttFrontLoadedSchema,
  TtCorrection,   ttCorrectionSchema,
  TtNullResult,   ttNullResultSchema,
  TtScaleDecay,   ttScaleDecaySchema,
  TtDenominator,  ttDenominatorSchema,
  TtAbsence,      ttAbsenceSchema,
  TtVerdictGrid,  ttVerdictGridSchema,
  TtEffectBars,   ttEffectBarsSchema,
} from './TrainTeacher';
// ── claude-liam-riff-the-outros — reel-local components ──
import { RiffSplit, riffSplitSchema, RiffLottery, riffLotterySchema } from './OutroRiff';
// ── claude-liam-dashboard-that-lied — reel-local components ──
import {
  DtlScale,     dtlScaleSchema,
  DtlChipGrid,  dtlChipGridSchema,
  DtlLayerStack, dtlLayerStackSchema,
} from './DashboardThatLied';
// ── finance skill — four chart shapes (SKILL.md §Shape logic, locked) ──
import {FinanceSankey,      financeSankeySchema}      from './scenes/FinanceSankey';
import {FinanceMirroredBar, financeMirroredBarSchema} from './scenes/FinanceMirroredBar';
import {FinanceStackedBar,  financeStackedBarSchema}  from './scenes/FinanceStackedBar';
import {FinanceDotPlot,     financeDotPlotSchema}     from './scenes/FinanceDotPlot';
// ── claude-liam-hesitant — Beat 2 executive summary, typed and corrected ──
import {BrutalistHesitantWriter, brutalistHesitantWriterSchema, brutalistHesitantWriterDemoDefaultProps} from './scenes/BrutalistHesitantWriter';
// ── fashionista modifier — photo-critique beat components ──
import {LookPlate,      lookPlateSchema}      from './scenes/LookPlate';
import {LookPlate916,   lookPlate916Schema}   from './scenes/LookPlate916';
import {ContactSheet,   contactSheetSchema}   from './scenes/ContactSheet';
import {ContactSheet916,contactSheet916Schema}from './scenes/ContactSheet916';
import {GitHubRepoHero,    gitHubRepoHeroSchema}    from './scenes/GitHubRepoHero';
import {GitHubCodeViewer,  gitHubCodeViewerSchema}  from './scenes/GitHubCodeViewer';
import {GitHubCodeDiff,    gitHubCodeDiffSchema}    from './scenes/GitHubCodeDiff';
import {GitHubCallChain,   gitHubCallChainSchema}   from './scenes/GitHubCallChain';
import {GitHubChurn,       gitHubChurnSchema}       from './scenes/GitHubChurn';
import {BadgeReveal}                               from './scenes/BadgeReveal';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Codex interface template library */}
      <Folder name="Codex-Templates">
      <Composition
        id="CodexComposerAsk"
        component={CodexComposerAsk}
        durationInFrames={240}
        fps={30}
        width={1920}
        height={1080}
        schema={codexComposerAskSchema}
        defaultProps={{
          command: 'Inspect this repository, explain the failing test, and implement the smallest verified fix.',
          topic: 'CODEX · REPOSITORY TASK',
          segment: 'Fix the failing test',
          workspace: 'bear-textbooks',
          runningText: 'Working in the repository…',
          output: ['Read AGENTS.md', 'Inspected the failing path', 'Implemented and verified the fix'],
          modelLabel: 'Codex',
          modeLabel: 'Local',
        }}
      />
      <Composition
        id="CodexWindow"
        component={CodexWindow}
        durationInFrames={180}
        fps={30}
        width={1920}
        height={1080}
        schema={codexWindowSchema}
        defaultProps={{
          view: 'report',
          title: 'Task complete',
          heading: 'What changed',
          lines: ['Made the smallest scoped edit', 'Preserved unrelated work', 'Ran the relevant verification'],
          workspace: 'bear-textbooks',
          fileLabel: 'src/example.ts',
          added: 12,
          removed: 3,
          statusLine: 'Checks passed',
        }}
      />
      <Composition
        id="CodexCodeBeat"
        component={CodexCodeBeat}
        durationInFrames={180}
        fps={30}
        width={1920}
        height={1080}
        schema={codexCodeBeatSchema}
        defaultProps={{
          title: 'src/validate.ts',
          code: "export const validate = (value: string) => {\n  if (!value.trim()) throw new Error('value required');\n  return value.trim();\n};",
          language: 'typescript',
          command: 'npm test -- validate',
          statusLine: '3 tests passed',
        }}
      />
      <Composition
        id="CodexCallout"
        component={CodexCallout}
        durationInFrames={180}
        fps={30}
        width={1920}
        height={1080}
        schema={codexCalloutSchema}
        defaultProps={{
          title: 'The repository is the context',
          body: 'Codex reads instructions, changes files, and verifies the result. The artifact is the work—not a chat answer.',
          label: 'DESIGN DECISION',
          workspace: 'bear-textbooks',
          target: 'diff',
        }}
      />
      <Composition
        id="CodexTitleOutro"
        component={CodexTitleOutro}
        durationInFrames={120}
        fps={30}
        width={1920}
        height={1080}
        schema={codexTitleOutroSchema}
        defaultProps={{title: 'Build it with Codex.', handle: '@NikBearBrown', subline: 'inspect · change · verify'}}
      />
      </Folder>
      <Composition
        id="BarChart"
        component={BarChart}
        durationInFrames={180}
        fps={30}
        width={1280}
        height={720}
        schema={barChartSchema}
        defaultProps={{
          title: 'Your model called 200 loans "99% safe." Count the ones that paid:',
          unit: '',
          accentIndex: 3,
          data: [
            {label: 'Predicted', value: 200},
            {label: 'Paid yr1', value: 188},
            {label: 'Paid yr2', value: 176},
            {label: 'Paid yr3', value: 170},
          ],
        }}
      />
      {/* The two accepted card forms — DESIGN-PRINCIPLES.md §1. SlateCard is deleted. */}
      <Composition
        id="FormACard"
        component={FormACard}
        durationInFrames={300}
        fps={30}
        width={3840}
        height={2160}
        schema={formACardSchema}
        defaultProps={formACardSchema.parse({})}
      />
      <Composition id="TypesetMath" component={TypesetMath}
        width={1920} height={1080} fps={30} durationInFrames={450}
        schema={typesetMathSchema} defaultProps={typesetMathSchema.parse({})} />
      <Composition id="TypesetMath916" component={TypesetMath}
        width={1080} height={1920} fps={30} durationInFrames={450}
        schema={typesetMathSchema} defaultProps={typesetMathSchema.parse({})} />
      <Composition id="ExecutedData" component={ExecutedData}
        width={1920} height={1080} fps={30} durationInFrames={450}
        schema={executedDataSchema} defaultProps={{title: 'Executed data', mode: 'table',
          rows: [{label: '0', value: 1, at: 0}], note: 'Supply actual evidence.', columnLabels: ['Index', 'Value']}} />
      <Composition id="ExecutedData916" component={ExecutedData}
        width={1080} height={1920} fps={30} durationInFrames={450}
        schema={executedDataSchema} defaultProps={{title: 'Executed data', mode: 'table',
          rows: [{label: '0', value: 1, at: 0}], note: 'Supply actual evidence.', columnLabels: ['Index', 'Value']}} />
      <Composition
        id="FormBCard"
        component={FormBCard}
        durationInFrames={300}
        fps={30}
        width={3840}
        height={2160}
        schema={formBCardSchema}
        defaultProps={formBCardSchema.parse({
          title: 'Form B',
          items: [
            { label: 'Name the thing', sub: 'one line of support' },
            { label: 'Name the next',  sub: 'one line of support' },
            { label: 'Name the last',  sub: 'one line of support' },
          ],
        })}
      />
      <Composition
        id="FormACard916"
        component={FormACard916}
        durationInFrames={300}
        fps={30}
        width={2160}
        height={3840}
        schema={formACard916Schema}
        defaultProps={formACard916Schema.parse({})}
      />
      <Composition
        id="FormBCard916"
        component={FormBCard916}
        durationInFrames={300}
        fps={30}
        width={2160}
        height={3840}
        schema={formBCard916Schema}
        defaultProps={formBCard916Schema.parse({
          title: 'Form B',
          items: [
            { label: 'Name the thing', sub: 'one line of support' },
            { label: 'Name the next',  sub: 'one line of support' },
            { label: 'Name the last',  sub: 'one line of support' },
          ],
        })}
      />
      {/* Ported 2026-08-30 — named by the public cut's own skills/docs. */}
      <Composition id="ClaudeMascotShortGrid" component={ClaudeMascotShortGrid}
        durationInFrames={450} fps={30} width={1080} height={1920}
        schema={claudeMascotShortGridSchema}
        defaultProps={claudeMascotShortGridSchema.parse({
          cells: [
            { animationName: 'wave',  caption: 'wave' },
            { animationName: 'think', caption: 'think' },
            { animationName: 'jump',  caption: 'jump' },
          ],
        })} />
      <Composition id="ClaudeMascotGrid" component={ClaudeMascotGrid}
        durationInFrames={300} fps={30} width={3840} height={2160}
        schema={claudeMascotGridSchema} defaultProps={claudeMascotGridSchema.parse({
          cells: [
            { animationName: 'idle',      caption: 'idle' },
            { animationName: 'wave',      caption: 'wave' },
            { animationName: 'nod',       caption: 'nod' },
            { animationName: 'think',     caption: 'think' },
            { animationName: 'type',      caption: 'type' },
            { animationName: 'bounce',    caption: 'bounce' },
            { animationName: 'stretch',   caption: 'stretch' },
            { animationName: 'jump',      caption: 'jump' },
            { animationName: 'celebrate', caption: 'celebrate' },
          ],
        })} />
      <Composition id="ClaudeMascotScene" component={ClaudeMascotScene}
        durationInFrames={300} fps={30} width={3840} height={2160}
        schema={claudeMascotSceneSchema} defaultProps={claudeMascotSceneSchema.parse({})} />
      <Composition id="DoodleChart" component={DoodleChart}
        durationInFrames={300} fps={30} width={3840} height={2160}
        schema={doodleChartSchema} defaultProps={doodleChartSchema.parse({
          kind: 'bar',
          title: 'Demo',
          data: [
            { label: 'One',   value: 3 },
            { label: 'Two',   value: 5 },
            { label: 'Three', value: 4 },
          ],
        })} />
      <Composition id="DoodleScene" component={DoodleScene}
        durationInFrames={300} fps={30} width={3840} height={2160}
        schema={doodleSceneSchema} defaultProps={doodleSceneSchema.parse({})} />
      <Composition id="GitHubSectionRail" component={GitHubSectionRail}
        durationInFrames={300} fps={30} width={3840} height={2160}
        schema={gitHubSectionRailSchema} defaultProps={gitHubSectionRailSchema.parse({})} />
      <Composition id="GitHubStructureMap" component={GitHubStructureMap}
        durationInFrames={300} fps={30} width={3840} height={2160}
        schema={gitHubStructureMapSchema} defaultProps={gitHubStructureMapSchema.parse({})} />
      <Composition id="ShellSession" component={ShellSession}
        durationInFrames={300} fps={30} width={3840} height={2160}
        schema={shellSessionSchema} defaultProps={shellSessionSchema.parse({})} />
      <Composition
        id="OutroSeries"
        component={OutroSeries}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
        schema={outroSeriesSchema}
        defaultProps={{eyebrow: 'CLAUDE COWORK', line: 'Part of the Claude Cowork series.'}}
      />
      <Composition
        id="OutroCTA"
        component={OutroCTA}
        durationInFrames={90}
        fps={30}
        width={1920}
        height={1080}
        schema={outroCtaSchema}
        defaultProps={{line: 'Like and subscribe for more.', handle: '@nikbearbrown'}}
      />
      <Composition
        id="BrutalistTerminalOpen"
        component={BrutalistTerminalOpen}
        durationInFrames={600}
        fps={30}
        width={1920}
        height={1080}
        schema={brutalistTerminalOpenSchema}
        defaultProps={{
          command: 'brutalist explainer-video "Why Cancer Cells Are Harder to Kill"',
          checklist: [
            '✓ palette   teardown  #FFFFFF/#2A1A0E/#C8102E',
            '✓ B00       BrutalistTerminalOpen',
            '✓ B99       BrutalistCommentCTA',
            '✓ voice     NikBearBrown',
            '✓ masters   16:9 + 9:16',
            '✓ factcheck FACTCHECK.md',
            '✓ layout    band-separation',
            '✓ gate      PASS',
          ],
          topic: 'CANCER BIOLOGY',
        }}
      />
      <Composition
        id="BrutalistTerminalOpen916"
        component={BrutalistTerminalOpen}
        durationInFrames={600}
        fps={30}
        width={1080}
        height={1920}
        schema={brutalistTerminalOpenSchema}
        defaultProps={{
          command: 'brutalist explainer-video "Why Cancer Cells Are Harder to Kill"',
          checklist: [
            '✓ palette   teardown',
            '✓ B00       BrutalistTerminalOpen',
            '✓ B99       BrutalistCommentCTA',
            '✓ voice     NikBearBrown',
            '✓ gate      PASS',
          ],
          topic: 'CANCER BIOLOGY',
        }}
      />
      <Composition
        id="BrutalistAdaptCLI"
        component={BrutalistAdaptCLI}
        durationInFrames={360}
        fps={30}
        width={1920}
        height={1080}
        schema={brutalistAdaptCLISchema}
        defaultProps={{
          lines: [
            '# every beat is tagged →  B00  B04  B12 …',
            '$ claude "swap B04 for a 9:16 diagram"',
            '$ claude "rewrite B07 for high-schoolers"',
          ],
          topic: 'CANCER BIOLOGY',
        }}
      />
      <Composition
        id="BrutalistAdaptCLI916"
        component={BrutalistAdaptCLI}
        durationInFrames={360}
        fps={30}
        width={1080}
        height={1920}
        schema={brutalistAdaptCLISchema}
        defaultProps={{
          lines: [
            '# every beat is tagged →  B00  B04  B12 …',
            '$ claude "swap B04 for a 9:16 diagram"',
            '$ claude "rewrite B07 for high-schoolers"',
          ],
          topic: 'CANCER BIOLOGY',
        }}
      />
      <Composition
        id="BrutalistCommentCTA"
        component={BrutalistCommentCTA}
        durationInFrames={450}
        fps={30}
        width={1920}
        height={1080}
        schema={brutalistCommentCTASchema}
        defaultProps={{
          filename: 'onda.ts',
          code: '// cancer-biology / apoptosis-resistance\n//\n// if this was useful, follow for more\n// @nikbearbrown  ·  brutalist.art\n',
          variant: 'A',
          topic: 'CANCER BIOLOGY',
        }}
      />
      <Composition
        id="BrutalistCommentCTA916"
        component={BrutalistCommentCTA}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        schema={brutalistCommentCTASchema}
        defaultProps={{
          filename: 'onda.ts',
          code: '// cancer-biology / apoptosis-resistance\n//\n// if this was useful, follow for more\n// @nikbearbrown  ·  brutalist.art\n',
          variant: 'A',
          topic: 'CANCER BIOLOGY',
        }}
      />
      <Composition
        id="MedhavyTerminalAsk"
        component={MedhavyTerminalAsk}
        durationInFrames={450}
        fps={30}
        width={1920}
        height={1080}
        schema={medhavyTerminalAskSchema}
        defaultProps={{
          command: 'claude "write a Manim scene:\n  photoelectric effect, Na (Φ=2.28 eV)\n  photons 700 / 546 / 300 nm\n  eject e⁻ if hν > Φ;  speed ∝ √(hν−Φ)"',
          topic: 'CLAUDE CODE · MANIM',
          segment: 'PHOTOELECTRIC EFFECT',
          runningText: 'generating scene…',
        }}
      />
      <Composition
        id="MedhavyTerminalAsk916"
        component={MedhavyTerminalAsk}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        schema={medhavyTerminalAskSchema}
        defaultProps={{
          command: 'claude "write a Manim scene:\n  photoelectric effect, Na (Φ=2.28 eV)\n  photons 700 / 546 / 300 nm\n  eject e⁻ if hν > Φ;  speed ∝ √(hν−Φ)"',
          topic: 'CLAUDE CODE · MANIM',
          segment: 'PHOTOELECTRIC EFFECT',
          runningText: 'generating scene…',
        }}
      />
      <Composition
        id="MedhavyCodeBlock"
        component={MedhavyCodeBlock}
        durationInFrames={450}
        fps={30}
        width={1920}
        height={1080}
        schema={medhavyCodeBlockSchema}
        defaultProps={{
          filename: 'photoelectric.py',
          segment: 'PHOTOELECTRIC EFFECT',
          topic: 'CLAUDE CODE · MANIM',
          code: '# photoelectric.py  —  Claude Code output\nPHI = 2.28          # eV  sodium work function\n\nclass PhotoelectricScene(Scene):\n    def construct(self):\n        for lam in [700, 546, 300]:\n            E = 1240 / lam\n            K = max(0.0, E - PHI)  # ← the physics\n            if K > 0:\n                self.play(GrowArrow(Arrow(ORIGIN, UP*np.sqrt(K))))',
        }}
      />
      <Composition
        id="MedhavyCodeBlock916"
        component={MedhavyCodeBlock}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        schema={medhavyCodeBlockSchema}
        defaultProps={{
          filename: 'photoelectric.py',
          segment: 'PHOTOELECTRIC EFFECT',
          topic: 'CLAUDE CODE · MANIM',
          code: '# photoelectric.py  —  Claude Code output\nPHI = 2.28          # eV  sodium work function\n\nclass PhotoelectricScene(Scene):\n    def construct(self):\n        for lam in [700, 546, 300]:\n            E = 1240 / lam\n            K = max(0.0, E - PHI)  # ← the physics\n            if K > 0:\n                self.play(GrowArrow(Arrow(ORIGIN, UP*np.sqrt(K))))',
        }}
      />
      <Composition
        id="SeisSpotlightOpen"
        component={SeisSpotlightOpen}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        schema={seisSpotlightOpenSchema}
        defaultProps={{eyebrow: 'Student spotlight', name: 'Ashlesha Donde', program: 'MS in Information Systems', term: 'Spring 2027', unit: 'Software Engineering and Information Systems', school: 'Northeastern University · College of Engineering', photo: '', photoCredit: '', logo: 'northeastern/official/notched-n-wordmark-red-black.svg'}}
      />
      <Composition
        id="SeisCard"
        component={SeisCard}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        schema={seisCardSchema}
        defaultProps={{label: 'Ashlesha Donde', lines: ['Technology is most powerful', 'when it is applied with purpose.'], emphasis: -1}}
      />
      <Composition
        id="SeisProfileCredit"
        component={SeisProfileCredit}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        schema={seisProfileCreditSchema}
        defaultProps={{name: 'Ashlesha Donde', role: 'MS in Information Systems · Spring 2027', links: [], storyUrl: 'https://coe.northeastern.edu/news/from-analytics-to-application-ashlesha-dondes-path-in-information-systems/', storyDate: 'April 21, 2026', storyAuthor: ''}}
      />
      <Composition
        id="SeisOutro"
        component={SeisOutro}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        schema={seisOutroSchema}
        defaultProps={{unit: 'Software Engineering and Information Systems', school: 'Northeastern University · College of Engineering', series: 'SEIS student spotlights', handle: '@nu_seis', url: '', logo: 'northeastern/official/notched-n-wordmark-red-black.svg'}}
      />
      <Composition
        id="SeisTribute"
        component={SeisTribute}
        durationInFrames={3816}
        fps={30}
        width={1920}
        height={1080}
        schema={seisTributeSchema}
        defaultProps={{title: 'For the Unconquerable Souls', dedication: 'for the international students of SEIS', credit: 'adapted from Invictus — William Ernest Henley (1875) · music by Nik Bear Brown', unit: 'Software Engineering and Information Systems · Northeastern University', titleFrames: 150, wallStart: 3335}}
      />
      <Composition
        id="SeisShowcase"
        component={SeisShowcase}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        schema={seisShowcaseSchema}
        defaultProps={{eyebrow: 'SEIS · student work', name: 'Naimisha Kaza', project: 'FitPath', line: 'AI health platform — AR coaching, meal scanning, telehealth', index: '1 / 9', photo: ''}}
      />
      <Composition
        id="SeisWall"
        component={SeisWall}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        schema={seisWallSchema}
        defaultProps={{lines: ['about 250 films', '36 fellows', 'four in five came through SEIS'], emphasis: 2, cols: 14}}
      />
      <Composition
        id="SeisStoriesRoll"
        component={SeisStoriesRoll}
        durationInFrames={12421}
        fps={30}
        width={1920}
        height={1080}
        schema={seisStoriesRollSchema}
        defaultProps={{title: 'Student Spotlights', subtitle: '112 stories · Software Engineering and Information Systems'}}
      />
      <Composition
        id="SeisReadAlong"
        component={SeisReadAlong}
        durationInFrames={8610}
        fps={30}
        width={1920}
        height={1080}
        schema={seisReadAlongSchema}
        defaultProps={{}}
      />
      <Composition
        id="SeisSongReadAlong"
        component={SeisSongReadAlong}
        durationInFrames={8610}
        fps={30}
        width={1920}
        height={1080}
        schema={seisSongReadAlongSchema}
        defaultProps={{}}
      />
      <Composition
        id="SeisQA"
        component={SeisQA}
        durationInFrames={390}
        fps={30}
        width={1920}
        height={1080}
        schema={seisQASchema}
        defaultProps={{question: 'What did the program change for you?', questionAudio: '', questionFrames: 90, clip: '', clipFrames: 300, name: 'Alum Name', program: 'MS Information Systems · SEIS', gradYear: '', title: '', company: '', captions: [], logo: 'seis/seis-button-logo.jpg', lockup: 'seis/seis-logo.png'}}
        calculateMetadata={({props}) => ({durationInFrames: props.questionFrames + props.clipFrames})}
      />
      <Composition
        id="SeisFilm"
        component={SeisFilm}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        schema={seisFilmSchema}
        defaultProps={{items: [], music: '', musicGain: 0.12}}
        calculateMetadata={({props}) => ({durationInFrames: Math.max(30, props.items.reduce((a, it) => a + it.frames, 0))})}
      />
      <Composition
        id="SeisLogoTechnique"
        component={SeisLogoTechnique}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        schema={seisLogoTechniqueSchema}
        defaultProps={{technique: 'spring-entrance', logo: 'seis/seis-logo.png', label: 'Spring Entrance', index: '1 / 17', markWidth: 0.46, square: false}}
      />
      <Composition
        id="MedhavyOpen"
        component={MedhavyOpen}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        schema={medhavyOpenSchema}
        defaultProps={{
          topic: 'MEDHAVY AI',
          lines: [
            'Medhavy AI',
            'Also known as Medhavi',
            'मेधावी (Medhavy): From Sanskrit, meaning',
            '"intelligent" or "intellectually brilliant"',
            '— the perfect name for our AI-powered',
            '  intelligent learning systems.',
          ],
        }}
      />
      <Composition
        id="MedhavyOpen916"
        component={MedhavyOpen}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        schema={medhavyOpenSchema}
        defaultProps={{
          topic: 'MEDHAVY AI',
          lines: [
            'Medhavy AI',
            'Also known as Medhavi',
            'मेधावी (Medhavy): From Sanskrit, meaning',
            '"intelligent" or "intellectually brilliant"',
            '— the perfect name for our AI-powered',
            '  intelligent learning systems.',
          ],
        }}
      />
      <Composition
        id="MedhavyOutro"
        component={MedhavyOutro}
        durationInFrames={240}
        fps={30}
        width={1920}
        height={1080}
        schema={medhavyOutroSchema}
        defaultProps={{
          brand: 'Medhavy',
          tagline: 'AI-powered intelligent learning systems',
          handle: '@MedhavyAI',
          url: 'medhavy.com',
        }}
      />
      <Composition
        id="MedhavyOutro916"
        component={MedhavyOutro}
        durationInFrames={240}
        fps={30}
        width={1080}
        height={1920}
        schema={medhavyOutroSchema}
        defaultProps={{
          brand: 'Medhavy',
          tagline: 'AI-powered intelligent learning systems',
          handle: '@MedhavyAI',
          url: 'medhavy.com',
        }}
      />
      <Composition
        id="NikBearBrownTerminalAsk"
        component={NikBearBrownTerminalAsk}
        durationInFrames={450}
        fps={30}
        width={1920}
        height={1080}
        schema={nikBearBrownTerminalAskSchema}
        defaultProps={{
          command: 'claude "write a Manim scene: photoelectric effect"',
          topic: 'CLAUDE CODE · MANIM',
          segment: 'PHOTOELECTRIC EFFECT',
          runningText: 'running simulation…',
        }}
      />
      <Composition
        id="NikBearBrownTerminalAsk916"
        component={NikBearBrownTerminalAsk}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        schema={nikBearBrownTerminalAskSchema}
        defaultProps={{
          command: 'claude "write a Manim scene: photoelectric effect"',
          topic: 'CLAUDE CODE · MANIM',
          segment: 'PHOTOELECTRIC EFFECT',
          runningText: 'running simulation…',
        }}
      />
      <Composition
        id="ClaudeComposerAsk"
        component={ClaudeComposerAsk}
        durationInFrames={900}
        calculateMetadata={({props}) => ({durationInFrames: Math.ceil(((props as any).durationSeconds ?? 30) * 30)})}
        fps={30}
        width={1920}
        height={1080}
        schema={claudeComposerAskSchema}
        defaultProps={{
          command: 'claude "write a Manim scene: photoelectric effect"',
          topic: 'CLAUDE CODE \u00b7 MANIM',
          segment: 'Photoelectric Effect',
          greeting: 'Hola, Bear',
          runningText: 'running simulation\u2026',
          folderLabel: '@NikBearBrown',
          modelLabel: 'Fable 5',
          effortLabel: 'High',
          placeholder: 'Type / for skills',
        }}
      />
      <Composition
        id="ClaudeComposerAsk916"
        component={ClaudeComposerAsk}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        schema={claudeComposerAskSchema}
        defaultProps={{
          command: 'claude "write a Manim scene: photoelectric effect"',
          topic: 'CLAUDE CODE \u00b7 MANIM',
          segment: 'Photoelectric Effect',
          greeting: 'Hola, Bear',
          runningText: 'running simulation\u2026',
          folderLabel: '@NikBearBrown',
          modelLabel: 'Fable 5',
          effortLabel: 'High',
          placeholder: 'Type / for skills',
        }}
      />
      <Composition
        id="NikBearBrownCodeBlock"
        component={NikBearBrownCodeBlock}
        durationInFrames={450}
        fps={30}
        width={1920}
        height={1080}
        schema={nikBearBrownCodeBlockSchema}
        defaultProps={{
          filename: 'sim.py',
          segment: 'SIMULATION',
          topic: 'CLAUDE CODE · MANIM',
          code: '# sim.py — Claude Code output\n# your code here',
        }}
      />
      <Composition
        id="NikBearBrownCodeBlock916"
        component={NikBearBrownCodeBlock}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        schema={nikBearBrownCodeBlockSchema}
        defaultProps={{
          filename: 'sim.py',
          segment: 'SIMULATION',
          topic: 'CLAUDE CODE · MANIM',
          code: '# sim.py — Claude Code output\n# your code here',
        }}
      />
      <Composition
        id="NikBearBrownOpen"
        component={NikBearBrownOpen}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        schema={nikBearBrownOpenSchema}
        defaultProps={{
          topic: 'NIK BEAR BROWN',
          lines: [
            'Nik Bear Brown',
            'Brutalist + Educational AI',
            'Build something. Take it apart.',
            'Explain how it actually works.',
            'Judge the design. Build better.',
          ],
        }}
      />
      <Composition
        id="NikBearBrownOpen916"
        component={NikBearBrownOpen}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        schema={nikBearBrownOpenSchema}
        defaultProps={{
          topic: 'NIK BEAR BROWN',
          lines: [
            'Nik Bear Brown',
            'Brutalist + Educational AI',
            'Build something. Take it apart.',
            'Explain how it actually works.',
            'Judge the design. Build better.',
          ],
        }}
      />
      <Composition
        id="NikBearBrownOutro"
        component={NikBearBrownOutro}
        durationInFrames={240}
        fps={30}
        width={1920}
        height={1080}
        schema={nikBearBrownOutroSchema}
        defaultProps={{
          brand: 'Nik Bear Brown',
          tagline: 'Brutalist + Educational AI',
          handle: '@NikBearBrown',
          url: 'nikbearbrown.com',
        }}
      />
      <Composition
        id="NikBearBrownOutro916"
        component={NikBearBrownOutro}
        durationInFrames={240}
        fps={30}
        width={1080}
        height={1920}
        schema={nikBearBrownOutroSchema}
        defaultProps={{
          brand: 'Nik Bear Brown',
          tagline: 'Brutalist + Educational AI',
          handle: '@NikBearBrown',
          url: 'nikbearbrown.com',
        }}
      />
      <Composition
        id="KokoroRosterCard"
        component={KokoroRosterCard}
        durationInFrames={240}
        fps={30}
        width={1920}
        height={1080}
        schema={kokoroRosterCardSchema}
        defaultProps={{
          name: 'Heart',
          code: 'af_heart',
          group: 'American',
          grade: 'A-',
          index: '1/28',
          topic: 'KOKORO — THE FULL 28',
        }}
      />
      <Composition
        id="KokoroRosterCard916"
        component={KokoroRosterCard}
        durationInFrames={240}
        fps={30}
        width={1080}
        height={1920}
        schema={kokoroRosterCardSchema}
        defaultProps={{
          name: 'Heart',
          code: 'af_heart',
          group: 'American',
          grade: 'A-',
          index: '1/28',
          topic: 'KOKORO — THE FULL 28',
        }}
      />

      {/* ── claude-medhavy season 1 — "Claude, For Educators" ── */}
      <Composition id="MedhavyConceptCard" component={MedhavyConceptCard}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={medhavyConceptCardSchema}
        defaultProps={{ sparkLine: 'A date, not a deficit.', heading: 'not a deficit', body: 'AI did not exist when you were in school.', evidenceNote: undefined }} />
      <Composition id="MedhavyTwoColumnCard" component={MedhavyTwoColumnCard}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={medhavyTwoColumnCardSchema}
        defaultProps={{ sparkLine: 'Draft, then judge.', leftHeader: 'what Claude does', leftItems: ['draft the plan', 'cite the standard', 'suggest levels'], rightHeader: 'what you do', rightItems: ['judge every line', 'catch the errors', 'decide what ships'] }} />
      <Composition id="MedhavyPredictCard" component={MedhavyPredictCard}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={medhavyPredictCardSchema}
        defaultProps={{ sparkLine: 'Commit before the reveal.', question: "What's the most likely failure mode?", commit: 'commit to an answer before the next beat' }} />
      {/* ── claude-musinique season 1 — "Claude, For the Indie" ── */}
      <Composition id="MusiniqueLanes" component={MusiniqueLanes}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={musiniqueLanesSchema}
        defaultProps={{ sparkLine: 'Three lanes, three jobs.' }} />
      <Composition id="MusiniqueSortBranch" component={MusiniqueSortBranch}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={musiniqueSortBranchSchema}
        defaultProps={{ sparkLine: 'Judgment stays in the room.' }} />
      <Composition id="MusiniqueMismatch" component={MusiniqueMismatch}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={musiniqueMismatchSchema}
        defaultProps={{ sparkLine: 'The mistake, named.' }} />
      <Composition id="MusiniqueHearingLimit" component={MusiniqueHearingLimit}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={musiniqueHearingLimitSchema}
        defaultProps={{ sparkLine: 'It cannot hear you.' }} />
      <Composition id="MusiniqueArsenal" component={MusiniqueArsenal}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={musiniqueArsenalSchema}
        defaultProps={{ sparkLine: 'This season is an arsenal.' }} />
      {/* ── musinique-bookend skill — silent 4K-matched intro/outro cards for a
           finished standalone film. width/height/fps come from calculateMetadata
           so musinique_bookend.py can hand each render the source's exact
           ffprobe'd canvas; base durationInFrames/fps/width/height below are the
           Studio preview defaults only. ── */}
      <Composition id="MusiniqueIntroCard" component={MusiniqueIntroCard}
        durationInFrames={75} fps={30} width={1920} height={1080}
        schema={musiniqueIntroCardSchema}
        defaultProps={musiniqueIntroCardDefaultProps}
        calculateMetadata={({props}) => ({
          durationInFrames: Math.max(1, Math.round(props.durationS * props.fps)),
          width: props.width,
          height: props.height,
          fps: props.fps,
        })} />
      <Composition id="MusiniqueIntroCardDemo" component={MusiniqueIntroCardDemo}
        durationInFrames={75} fps={30} width={1920} height={1080}
        schema={musiniqueIntroCardDemoSchema}
        defaultProps={musiniqueIntroCardDemoDefaultProps}
        calculateMetadata={({props}) => ({
          durationInFrames: Math.max(1, Math.round(props.durationS * props.fps)),
          width: props.width,
          height: props.height,
          fps: props.fps,
        })} />
      <Composition id="MusiniqueOutroCard" component={MusiniqueOutroCard}
        durationInFrames={75} fps={30} width={1920} height={1080}
        schema={musiniqueOutroCardSchema}
        defaultProps={musiniqueOutroCardDefaultProps}
        calculateMetadata={({props}) => ({
          durationInFrames: Math.max(1, Math.round(props.durationS * props.fps)),
          width: props.width,
          height: props.height,
          fps: props.fps,
        })} />
      <Composition id="MusiniqueOutroCardDemo" component={MusiniqueOutroCardDemo}
        durationInFrames={90} fps={30} width={1920} height={1080}
        schema={musiniqueOutroCardDemoSchema}
        defaultProps={musiniqueOutroCardDemoDefaultProps}
        calculateMetadata={({props}) => ({
          durationInFrames: Math.max(1, Math.round(props.durationS * props.fps)),
          width: props.width,
          height: props.height,
          fps: props.fps,
        })} />
      <Composition id="ClaudeVerdictArtifact" component={ClaudeVerdictArtifact}
        durationInFrames={1020} fps={30} width={1920} height={1080}
        calculateMetadata={({props}) => ({durationInFrames: Math.ceil(((props as any).durationSeconds ?? 34) * 30)})}
        schema={claudeVerdictArtifactSchema}
        defaultProps={{
          artifactTitle: 'Verdict',
          artifactHeading: 'The split',
          artifactLines: [
            'Chat: synchronous judgment — you\'re in the loop every step.',
            'Cowork: asynchronous recipes — folder + instructions + schedule.',
            'Code: the pipeline room — skills, gates, and systems you own.',
          ],
        }} />
      <Composition id="ClaudeVerdictArtifact916" component={ClaudeVerdictArtifact916}
        durationInFrames={360} fps={30} width={1080} height={1920}
        schema={claudeVerdictArtifact916Schema}
        defaultProps={{
          artifactTitle: 'Verdict',
          artifactHeading: 'The split',
          artifactLines: [
            'Chat: synchronous judgment — you\'re in the loop every step.',
            'Cowork: asynchronous recipes — folder + instructions + schedule.',
            'Code: the pipeline room — skills, gates, and systems you own.',
          ],
        }} />
      <Composition id="ClaudeTitleOutro" component={ClaudeTitleOutro}
        durationInFrames={180} fps={30} width={1920} height={1080}
        calculateMetadata={({props}) => ({durationInFrames: Math.ceil(((props as any).durationSeconds ?? 6) * 30)})}
        schema={claudeTitleOutroSchema}
        defaultProps={claudeTitleOutroSchema.parse({})} />
      {/* claude-liam — adaptive-therapy-revolution */}
      <Composition id="ClaudeCodeBeat" component={ClaudeCodeBeat}
        durationInFrames={300} fps={30} width={1920} height={1080}
        calculateMetadata={({props}) => ({durationInFrames: Math.ceil(((props as any).durationSeconds ?? 10) * 30)})}
        schema={claudeCodeBeatSchema}
        defaultProps={{
          title: 'script.py',
          code: '# code here',
          sparkLine: 'The code speaks.',
        }} />
      <Composition id="ClaudeWindow" component={ClaudeWindow}
        durationInFrames={360} fps={30} width={1920} height={1080}
        schema={claudeWindowSchema}
        defaultProps={{
          view: 'artifact',
          artifactTitle: 'Verdict',
          artifactHeading: 'The verdict',
          artifactLines: ['Evidence line one.', 'Evidence line two.'],
          sparkLine: 'Control, not cure.',
        }} />
      {/* ── claude-liam — 1hr-cowork ── */}
      <Composition id="CoworkHourClock" component={CoworkHourClock}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={coworkHourClockSchema}
        defaultProps={{ activeWedge: 0, label: 'The sixty-minute plan.', handle: '@NikBearBrown' }} />
      {/* E2 — On Schedule */}
      <Composition id="OnScheduleRepurpose" component={OnScheduleRepurpose}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onScheduleRepurposeSchema}
        defaultProps={{ sparkLine: 'One take, every platform.' }} />
      <Composition id="OnScheduleDigest" component={OnScheduleDigest}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onScheduleDigestSchema}
        defaultProps={{ sparkLine: 'Start with the digest.' }} />
      <Composition id="OnScheduleOvernight" component={OnScheduleOvernight}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onScheduleOvernightSchema}
        defaultProps={{ sparkLine: 'Overnight, the homework.' }} />
      <Composition id="OnScheduleFinePrint" component={OnScheduleFinePrint}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onScheduleFinePrintSchema}
        defaultProps={{ sparkLine: 'The fine print, out loud.' }} />
      <Composition id="OnScheduleRedLine" component={OnScheduleRedLine}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onScheduleRedLineSchema}
        defaultProps={{ sparkLine: 'Drafts, not decisions.' }} />
      {/* E3 — Sourced */}
      <Composition id="SourcedExhibit" component={SourcedExhibit}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={sourcedExhibitSchema}
        defaultProps={{ sparkLine: 'The exhibit, on screen.' }} />
      <Composition id="SourcedLaundering" component={SourcedLaundering}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={sourcedLaunderingSchema}
        defaultProps={{ sparkLine: 'Why the lie works.' }} />
      <Composition id="SourcedSorting" component={SourcedSorting}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={sourcedSortingSchema}
        defaultProps={{ sparkLine: 'Not everything in it is false.' }} />
      <Composition id="SourcedSkillFile" component={SourcedSkillFile}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={sourcedSkillFileSchema}
        defaultProps={{ sparkLine: 'Three tiers, one rule.' }} />
      <Composition id="SourcedNoVerdict" component={SourcedNoVerdict}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={sourcedNoVerdictSchema}
        defaultProps={{ sparkLine: 'No source, no verdict.' }} />
      {/* E4 — In Your Voice */}
      <Composition id="InYourVoiceSkillFile" component={InYourVoiceSkillFile}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={inYourVoiceSkillFileSchema}
        defaultProps={{ sparkLine: 'The file, open.' }} />
      <Composition id="InYourVoiceSpecificity" component={InYourVoiceSpecificity}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={inYourVoiceSpecificitySchema}
        defaultProps={{ sparkLine: 'Context in, craft out.' }} />
      <Composition id="InYourVoiceLyricFile" component={InYourVoiceLyricFile}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={inYourVoiceLyricFileSchema}
        defaultProps={{ sparkLine: 'Craft rules are not caption rules.' }} />
      <Composition id="InYourVoicePaper" component={InYourVoicePaper}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={inYourVoicePaperSchema}
        defaultProps={{ sparkLine: 'The paper, read out loud.' }} />
      <Composition id="InYourVoiceMoat" component={InYourVoiceMoat}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={inYourVoiceMoatSchema}
        defaultProps={{ sparkLine: 'The moat is the voice.' }} />
      {/* E5 — On Your Catalog */}
      <Composition id="OnCatalogGrid" component={OnCatalogGrid}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onCatalogGridSchema}
        defaultProps={{ sparkLine: 'Thirty songs, one view.' }} />
      <Composition id="OnCatalogHabits" component={OnCatalogHabits}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onCatalogHabitsSchema}
        defaultProps={{ sparkLine: 'Your moves, cited back.' }} />
      <Composition id="OnCatalogThreads" component={OnCatalogThreads}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onCatalogThreadsSchema}
        defaultProps={{ sparkLine: 'The threads worth chasing.' }} />
      <Composition id="OnCatalogReads" component={OnCatalogReads}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onCatalogReadsSchema}
        defaultProps={{ sparkLine: 'What it reads, what it won\'t.' }} />
      <Composition id="OnCatalogData" component={OnCatalogData}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onCatalogDataSchema}
        defaultProps={{ sparkLine: 'Data in, data stays.' }} />
      {/* E6 — On the Pitch */}
      <Composition id="OnPitchHomework" component={OnPitchHomework}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onPitchHomeworkSchema}
        defaultProps={{ sparkLine: 'Overnight, the homework.' }} />
      <Composition id="OnPitchDraft" component={OnPitchDraft}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onPitchDraftSchema}
        defaultProps={{ sparkLine: 'The pitch, drafted.' }} />
      <Composition id="OnPitchMountain" component={OnPitchMountain}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onPitchMountainSchema}
        defaultProps={{ sparkLine: 'Five docs, one machine.' }} />
      <Composition id="OnPitchScam" component={OnPitchScam}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onPitchScamSchema}
        defaultProps={{ sparkLine: 'Guaranteed means scam.' }} />
      <Composition id="OnPitchVerify" component={OnPitchVerify}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={onPitchVerifySchema}
        defaultProps={{ sparkLine: 'Every claim through the filter.' }} />
      {/* E7 — In Your Hands */}
      <Composition id="InYourHandsDeck" component={InYourHandsDeck}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={inYourHandsDeckSchema}
        defaultProps={{ sparkLine: 'The deck, assembled.' }} />
      <Composition id="InYourHandsRedLine" component={InYourHandsRedLine}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={inYourHandsRedLineSchema}
        defaultProps={{ sparkLine: 'What never delegates.' }} />
      <Composition id="InYourHandsBotVsBot" component={InYourHandsBotVsBot}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={inYourHandsBotVsBotSchema}
        defaultProps={{ sparkLine: 'Bot versus bot, said plainly.' }} />
      <Composition id="InYourHandsCosts" component={InYourHandsCosts}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={inYourHandsCostsSchema}
        defaultProps={{ sparkLine: 'The costs, restated.' }} />
      <Composition id="InYourHandsSubscription" component={InYourHandsSubscription}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={inYourHandsSubscriptionSchema}
        defaultProps={{ sparkLine: 'The subscription you keep.' }} />
      {/* ── claude-liam — adaptive-therapy-revolution (full 11-beat reel) ── */}
      <Composition
        id="AdaptiveTherapyRevolution"
        component={AdaptiveTherapyRevolution}
        durationInFrames={ATR_TOTAL_FRAMES}
        fps={30}
        width={1280}
        height={720}
      />
      {/* ── claude-liam — cancer-biology-all batch retrofit ── */}
      <Composition id="CancerDisparitiesZipCode" component={CancerDisparitiesZipCode} durationInFrames={CancerDisparitiesZipCode_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="CancerDormancyRecurrence" component={CancerDormancyRecurrence} durationInFrames={CancerDormancyRecurrence_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="CarTSolidTumorBarrier" component={CarTSolidTumorBarrier} durationInFrames={CarTSolidTumorBarrier_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="ClonalResistancePrediction" component={ClonalResistancePrediction} durationInFrames={ClonalResistancePrediction_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="CtdnaMrdDetection" component={CtdnaMrdDetection} durationInFrames={CtdnaMrdDetection_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="MetastaticCascadeBottleneck" component={MetastaticCascadeBottleneck} durationInFrames={MetastaticCascadeBottleneck_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="NeoantigenaVaccinePipeline" component={NeoantigenaVaccinePipeline} durationInFrames={NeoantigenaVaccinePipeline_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="OncolyticVirotherapy" component={OncolyticVirotherapy} durationInFrames={OncolyticVirotherapy_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="PfsSurrogateEndpoint" component={PfsSurrogateEndpoint} durationInFrames={PfsSurrogateEndpoint_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="PreMetastaticNiche" component={PreMetastaticNiche} durationInFrames={PreMetastaticNiche_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="TumorHeterogeneityTracerx" component={TumorHeterogeneityTracerx} durationInFrames={TumorHeterogeneityTracerx_FRAMES} fps={30} width={1280} height={720} />
      {/* ── claude-explainer — cowork-setup ── */}
      <Composition id="CoworkSetup" component={CoworkSetup} durationInFrames={CoworkSetup_FRAMES} fps={30} width={1280} height={720} />
          {/* ── ruben-substack batch ── */}
      <Composition id="ChatgptCopiedClaude" component={ChatgptCopiedClaude} durationInFrames={ChatgptCopiedClaude_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="DontUseClaudeFable5" component={DontUseClaudeFable5} durationInFrames={DontUseClaudeFable5_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="Learn80OfClaudeCoworkIn20Minutes" component={Learn80OfClaudeCoworkIn20Minutes} durationInFrames={Learn80OfClaudeCoworkIn20Minutes_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="WhyAiWillFail" component={WhyAiWillFail} durationInFrames={WhyAiWillFail_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="ClaudeLinkedin" component={ClaudeLinkedin} durationInFrames={ClaudeLinkedin_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="TheClaudeCodeBible" component={TheClaudeCodeBible} durationInFrames={TheClaudeCodeBible_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="IReplacedMyself" component={IReplacedMyself} durationInFrames={IReplacedMyself_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="HowToUseYourPersonalAiAtWork" component={HowToUseYourPersonalAiAtWork} durationInFrames={HowToUseYourPersonalAiAtWork_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="S" component={S} durationInFrames={S_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="ClaudeRoadmap" component={ClaudeRoadmap} durationInFrames={ClaudeRoadmap_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="AiIsASlotMachine" component={AiIsASlotMachine} durationInFrames={AiIsASlotMachine_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="IShookHandsWithANobelPrize" component={IShookHandsWithANobelPrize} durationInFrames={IShookHandsWithANobelPrize_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="HowToMakePerfectSpreadsheets" component={HowToMakePerfectSpreadsheets} durationInFrames={HowToMakePerfectSpreadsheets_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="HowToBeatAiOnceItInevitably" component={HowToBeatAiOnceItInevitably} durationInFrames={HowToBeatAiOnceItInevitably_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="HowToRotYourBrainWithAi" component={HowToRotYourBrainWithAi} durationInFrames={HowToRotYourBrainWithAi_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="ClaudeConnectors" component={ClaudeConnectors} durationInFrames={ClaudeConnectors_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="Prompt47" component={Prompt47} durationInFrames={Prompt47_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="ImClaudeCertified" component={ImClaudeCertified} durationInFrames={ImClaudeCertified_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="YoureJustATextFile" component={YoureJustATextFile} durationInFrames={YoureJustATextFile_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="ItsNotXItsY" component={ItsNotXItsY} durationInFrames={ItsNotXItsY_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="EveryoneWantsOneAi" component={EveryoneWantsOneAi} durationInFrames={EveryoneWantsOneAi_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="ClaudeDesign" component={ClaudeDesign} durationInFrames={ClaudeDesign_FRAMES} fps={30} width={1280} height={720} />
      <Composition id="ClaudeForDummies" component={ClaudeForDummies} durationInFrames={ClaudeForDummies_FRAMES} fps={30} width={1280} height={720} />
      {/* ── claude-liam — math-of-being-afraid-together figures ── */}
      <Composition id="HorrorParadox" component={HorrorParadox}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={horrorParadoxSchema}
        defaultProps={{ sparkLine: 'The gap is the thing to explain.' }} />
      <Composition id="HorrorAxiom" component={HorrorAxiom}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={horrorAxiomSchema}
        defaultProps={{ sparkLine: 'A biological cheat code.' }} />
      <Composition id="HorrorComplication" component={HorrorComplication}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={horrorComplicationSchema}
        defaultProps={{ sparkLine: 'Panic transmits before the monster does.' }} />
      <Composition id="HorrorEquation" component={HorrorEquation}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={horrorEquationSchema}
        defaultProps={{ sparkLine: 'Design the safety net. Then take it away.' }} />
      <Composition id="HorrorAlphaHero" component={HorrorAlphaHero}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={horrorAlphaHeroSchema}
        defaultProps={{ sparkLine: 'Structural inability to fight back.' }} />
      <Composition id="HorrorTriptych" component={HorrorTriptych}
        durationInFrames={360} fps={30} width={1920} height={1080}
        schema={horrorTriptychSchema}
        defaultProps={{ sparkLine: 'Information and connection, not polygons.' }} />
      <Composition id="HorrorModelBreaks" component={HorrorModelBreaks}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={horrorModelBreaksSchema}
        defaultProps={{ sparkLine: 'The fraction cannot measure laughter.' }} />
      <Composition id="HorrorProofSpine" component={HorrorProofSpine}
        durationInFrames={360} fps={30} width={1920} height={1080}
        schema={horrorProofSpineSchema}
        defaultProps={{ sparkLine: 'The distance between you.' }} />
      {/* ── claude-liam — sleeper-agents figures ── */}
      <Composition id="SleeperAgentsBehaviorSwitch" component={SleeperAgentsBehaviorSwitch}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={sleeperAgentsBehaviorSwitchSchema}
        defaultProps={{ sparkLine: 'Same weights. Two modes.' }} />
      <Composition id="SleeperAgentsBehaviorSwitch916" component={SleeperAgentsBehaviorSwitch916}
        durationInFrames={450} fps={30} width={1080} height={1920}
        schema={sleeperAgentsBehaviorSwitch916Schema}
        defaultProps={{ sparkLine: 'Same weights. Two modes.' }} />
      <Composition id="SleeperAgentsExperiment" component={SleeperAgentsExperiment}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={sleeperAgentsExperimentSchema}
        defaultProps={{ sparkLine: '3,000 steps. Still there.' }} />
      <Composition id="SleeperAgentsExperiment916" component={SleeperAgentsExperiment916}
        durationInFrames={450} fps={30} width={1080} height={1920}
        schema={sleeperAgentsExperiment916Schema}
        defaultProps={{ sparkLine: '3,000 steps. Still there.' }} />
      <Composition id="SleeperAgentsResult" component={SleeperAgentsResult}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={sleeperAgentsResultSchema}
        defaultProps={{ sparkLine: 'More training → more hidden.' }} />
      <Composition id="SleeperAgentsResult916" component={SleeperAgentsResult916}
        durationInFrames={450} fps={30} width={1080} height={1920}
        schema={sleeperAgentsResult916Schema}
        defaultProps={{ sparkLine: 'More training → more hidden.' }} />
      {/* ── claude-liam — how-we-claude-code figures ── */}
      <Composition id="HowWeCode-Phase1" component={HowWeCode_Phase1}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={howWeCodePhase1Schema}
        defaultProps={{ sparkLine: 'Think before you build.' }} />
      <Composition id="HowWeCode-Phase2" component={HowWeCode_Phase2}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={howWeCodePhase2Schema}
        defaultProps={{ sparkLine: 'Diverge before you converge.' }} />
      <Composition id="HowWeCode-Phase3" component={HowWeCode_Phase3}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={howWeCodePhase3Schema}
        defaultProps={{ sparkLine: 'The test suite is the output.' }} />
      {/* ── claude-liam — three-principals figures ── */}
      <Composition id="PrincipalsNaiveView" component={PrincipalsNaiveView}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={principalsNaiveViewSchema}
        defaultProps={{ sparkLine: 'Three, not one.' }} />
      <Composition id="PrincipalsHierarchy" component={PrincipalsHierarchy}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={principalsHierarchySchema}
        defaultProps={{ sparkLine: 'Authority by design.' }} />
      <Composition id="PrincipalsOperatorBounds" component={PrincipalsOperatorBounds}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={principalsOperatorBoundsSchema}
        defaultProps={{ sparkLine: 'Restrict yes. Weaponize never.' }} />
      {/* ── claude-liam — ai-skill-formation figures ── */}
      {/* ── claude-liam — sycophancy-to-subterfuge figures ── */}
      <Composition id="SycGradientSpectrum" component={SycGradientSpectrum}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={sycGradientSpectrumSchema}
        defaultProps={{ sparkLine: 'Not a UX problem.' }} />
      <Composition id="SycCurriculumStages" component={SycCurriculumStages}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={sycCurriculumStagesSchema}
        defaultProps={{ sparkLine: 'Same drive. Different budget.' }} />
      <Composition id="SycWatcherWatched" component={SycWatcherWatched}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={sycWatcherWatchedSchema}
        defaultProps={{ sparkLine: 'The watcher is being watched.' }} />
      <Composition id="AiSkillStudyDesign" component={AiSkillStudyDesign}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={aiSkillStudyDesignSchema}
        defaultProps={{ sparkLine: '52 developers. One variable.' }} />
      <Composition id="AiSkillTreatmentEffect" component={AiSkillTreatmentEffect}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={aiSkillTreatmentEffectSchema}
        defaultProps={{ panel: 'A', sparkLine: 'Faster. Not significantly.' }} />
      <Composition id="AiSkillUsageModes" component={AiSkillUsageModes}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={aiSkillUsageModesSchema}
        defaultProps={{ phase: 'intro', sparkLine: 'HOW matters more than WHETHER.' }} />
      {/* ── claude-liam — teaching-claude-why figures ── */}
      <Composition id="TeachClaudeFig1" component={TeachClaudeFig1}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={teachClaudeFig1Schema}
        defaultProps={{ sparkLine: 'Factor of three. No eval data.' }} />
      <Composition id="TeachClaudeFig2" component={TeachClaudeFig2}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={teachClaudeFig2Schema}
        defaultProps={{ sparkLine: 'Same prompts. Different results.', phase: 'baseline' }} />
      <Composition id="TeachClaudeFig3" component={TeachClaudeFig3}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={teachClaudeFig3Schema}
        defaultProps={{ sparkLine: '28x less data. Better score.' }} />
      <Composition id="TeachClaudeFig4" component={TeachClaudeFig4}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={teachClaudeFig4Schema}
        defaultProps={{ sparkLine: 'Not the reward. The pre-training.' }} />
      <Composition id="TeachClaudeFig5" component={TeachClaudeFig5}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={teachClaudeFig5Schema}
        defaultProps={{ sparkLine: 'More admirable. Less misaligned.' }} />
      <Composition id="TeachClaudeFig6" component={TeachClaudeFig6}
        durationInFrames={450} fps={30} width={1920} height={1080}
        schema={teachClaudeFig6Schema}
        defaultProps={{ sparkLine: 'Richer context. Faster alignment.' }} />
      {/* ── claude-liam — coding-agents-social-sciences figures ── */}
      <Composition id="CodingAgentsFig1Loop" component={CodingAgentsFig1Loop}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={codingAgentsFig1LoopSchema}
        defaultProps={{ sparkLine: 'Chatbots suggest. Agents run.' }} />
      <Composition id="CodingAgentsFig2Gradient" component={CodingAgentsFig2Gradient}
        durationInFrames={570} fps={30} width={1920} height={1080}
        schema={codingAgentsFig2GradientSchema}
        defaultProps={{ sparkLine: 'Everyone uses AI. Not everyone lets it run.' }} />
      <Composition id="CodingAgentsFig3Who" component={CodingAgentsFig3Who}
        durationInFrames={570} fps={30} width={1920} height={1080}
        schema={codingAgentsFig3WhoSchema}
        defaultProps={{ sparkLine: 'The agent era is opening more unequal than the chatbot era.' }} />
      <Composition id="CodingAgentsFig4Use" component={CodingAgentsFig4Use}
        durationInFrames={480} fps={30} width={1920} height={1080}
        schema={codingAgentsFig4UseSchema}
        defaultProps={{ sparkLine: 'The adoption is about code. Not prose.' }} />
      <Composition id="CodingAgentsFig5Ladder" component={CodingAgentsFig5Ladder}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={codingAgentsFig5LadderSchema}
        defaultProps={{ sparkLine: "Agents launch projects. They don't finish papers." }} />
      <Composition id="CodingAgentsFig6Paradox" component={CodingAgentsFig6Paradox}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={codingAgentsFig6ParadoxSchema}
        defaultProps={{ sparkLine: 'Good for my papers. Unclear for my science.' }} />
      {/* ── claude-liam — economic-index-cadences figures ── */}
      <Composition id="CadencesFig1Clock" component={CadencesFig1Clock}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={cadencesFig1ClockSchema}
        defaultProps={{ sparkLine: 'Morning news. Evening recipes. Night advice.' }} />
      <Composition id="CadencesFig2Tax" component={CadencesFig2Tax}
        durationInFrames={390} fps={30} width={1920} height={1080}
        schema={cadencesFig2TaxSchema}
        defaultProps={{ sparkLine: 'Eight times the average. One day.' }} />
      <Composition id="CadencesFig3Artifacts" component={CadencesFig3Artifacts}
        durationInFrames={510} fps={30} width={1920} height={1080}
        schema={cadencesFig3ArtifactsSchema}
        defaultProps={{ sparkLine: '93% of conversations. Something to show.' }} />
      <Composition id="CadencesFig4Compute" component={CadencesFig4Compute}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={cadencesFig4ComputeSchema}
        defaultProps={{ sparkLine: 'More from Claude. More from you.' }} />
      <Composition id="CadencesFig5Leash" component={CadencesFig5Leash}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={cadencesFig5LeashSchema}
        defaultProps={{ sparkLine: 'The product sets the leash length.' }} />
      <Composition id="CadencesFig6Tide" component={CadencesFig6Tide}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={cadencesFig6TideSchema}
        defaultProps={{ sparkLine: 'A rising tide. Same increment everywhere.' }} />
      <Composition id="CadencesFig7Jobs" component={CadencesFig7Jobs}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={cadencesFig7JobsSchema}
        defaultProps={{ sparkLine: "It'll happen to someone junior." }} />
      <Composition id="CadencesFig8Paradox" component={CadencesFig8Paradox}
        durationInFrames={570} fps={30} width={1920} height={1080}
        schema={cadencesFig8ParadoxSchema}
        defaultProps={{ sparkLine: 'Delegate more. Expect better. Not worse.' }} />
      <Composition id="CadencesFig9Gender" component={CadencesFig9Gender}
        durationInFrames={420} fps={30} width={1920} height={1080}
        schema={cadencesFig9GenderSchema}
        defaultProps={{ sparkLine: 'More time. More iterative. More collaborative.' }} />
      <Composition id="CadencesFig10Dream" component={CadencesFig10Dream}
        durationInFrames={420} fps={30} width={1920} height={1080}
        schema={cadencesFig10DreamSchema}
        defaultProps={{ sparkLine: 'Not replacement. Not rescue. Collaboration.' }} />
      {/* ── claude-liam — 81k-interviews figures ── */}
      <Composition id="WantFig1Scale" component={WantFig1Scale}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={wantFig1ScaleSchema}
        defaultProps={{ sparkLine: 'Largest qualitative study ever.' }} />
      <Composition id="WantFig2Hopes" component={WantFig2Hopes}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={wantFig2HopesSchema}
        defaultProps={{ sparkLine: 'A third want time, not work.' }} />
      <Composition id="WantFig3Delivered" component={WantFig3Delivered}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={wantFig3DeliveredSchema}
        defaultProps={{ sparkLine: '81% say yes. But look at the smallest bar.' }} />
      <Composition id="WantFig4Fears" component={WantFig4Fears}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={wantFig4FearsSchema}
        defaultProps={{ sparkLine: 'Jobs fear predicts everything.' }} />
      <Composition id="WantFig5LightShade" component={WantFig5LightShade}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={wantFig5LightShadeSchema}
        defaultProps={{ sparkLine: 'Same person. Hope and fear.' }} />
      <Composition id="WantFig6aWorld" component={WantFig6aWorld}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={wantFig6aWorldSchema}
        defaultProps={{ sparkLine: 'The wealthy worry more.' }} />
      <Composition id="WantFig6bQuadrant" component={WantFig6bQuadrant}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={wantFig6bQuadrantSchema}
        defaultProps={{ sparkLine: 'Same AI. Different stakes.' }} />
      <Composition id="WantQuote" component={WantQuote}
        durationInFrames={180} fps={30} width={1920} height={1080}
        schema={wantQuoteSchema}
        defaultProps={{
          quote: 'I left work on time and picked up my daughter from daycare.',
          attribution: 'Software engineer, Japan',
          sparkLine: 'Time back.',
        }} />
      {/* ── claude-liam — 81k-interviews figures 916 (portrait) ── */}
      <Composition id="WantFig1Scale916" component={WantFig1Scale916}
        durationInFrames={300} fps={30} width={1080} height={1920}
        schema={wantFig1Scale916Schema}
        defaultProps={{ sparkLine: 'Largest qualitative study ever.' }} />
      <Composition id="WantFig2Hopes916" component={WantFig2Hopes916}
        durationInFrames={300} fps={30} width={1080} height={1920}
        schema={wantFig2Hopes916Schema}
        defaultProps={{ sparkLine: 'A third want time, not work.' }} />
      <Composition id="WantFig3Delivered916" component={WantFig3Delivered916}
        durationInFrames={300} fps={30} width={1080} height={1920}
        schema={wantFig3Delivered916Schema}
        defaultProps={{ sparkLine: '81% say yes. But look at the smallest bar.' }} />
      <Composition id="WantFig4Fears916" component={WantFig4Fears916}
        durationInFrames={300} fps={30} width={1080} height={1920}
        schema={wantFig4Fears916Schema}
        defaultProps={{ sparkLine: 'Jobs fear predicts everything.' }} />
      <Composition id="WantFig6aWorld916" component={WantFig6aWorld916}
        durationInFrames={300} fps={30} width={1080} height={1920}
        schema={wantFig6aWorld916Schema}
        defaultProps={{ sparkLine: 'The wealthy worry more.' }} />
      <Composition id="WantFig6bQuadrant916" component={WantFig6bQuadrant916}
        durationInFrames={300} fps={30} width={1080} height={1920}
        schema={wantFig6bQuadrant916Schema}
        defaultProps={{ sparkLine: 'Same AI. Different stakes.' }} />
      <Composition id="WantQuote916" component={WantQuote916}
        durationInFrames={180} fps={30} width={1080} height={1920}
        schema={wantQuote916Schema}
        defaultProps={{
          quote: 'I left work on time and picked up my daughter from daycare.',
          attribution: 'Software engineer, Japan',
          sparkLine: 'Time back.',
        }} />
      {/* ── claude-liam — claude-values-axes figures ── */}
      <Composition id="ValuesCompressionFunnel" component={ValuesCompressionFunnel}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={valuesCompressionFunnelSchema}
        defaultProps={{ sparkLine: 'Compression, not the whole picture.' }} />
      <Composition id="ValuesFourAxes" component={ValuesFourAxes}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={valuesFourAxesSchema}
        defaultProps={{ sparkLine: 'Four spectrums. One model.' }} />
      <Composition id="ValuesModelProfiles" component={ValuesModelProfiles}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={valuesModelProfilesSchema}
        defaultProps={{ sparkLine: 'The method tracks something real.' }} />
      <Composition id="ValuesLanguageProfiles" component={ValuesLanguageProfiles}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={valuesLanguageProfilesSchema}
        defaultProps={{ sparkLine: 'Biggest spread: Warmth to Rigor.' }} />
      <Composition id="ValuesSplitScreen" component={ValuesSplitScreen}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={valuesSplitScreenSchema}
        defaultProps={{ sparkLine: 'Measurable, not random noise.' }} />
      {/* ── claude-liam — claude-values-axes figures 916 (portrait) ── */}
      <Composition id="ValuesCompressionFunnel916" component={ValuesCompressionFunnel916}
        durationInFrames={300} fps={30} width={1080} height={1920}
        schema={valuesCompressionFunnel916Schema}
        defaultProps={{ sparkLine: 'Compression, not the whole picture.' }} />
      <Composition id="ValuesFourAxes916" component={ValuesFourAxes916}
        durationInFrames={300} fps={30} width={1080} height={1920}
        schema={valuesFourAxes916Schema}
        defaultProps={{ sparkLine: 'Four spectrums. One model.' }} />
      <Composition id="ValuesModelProfiles916" component={ValuesModelProfiles916}
        durationInFrames={300} fps={30} width={1080} height={1920}
        schema={valuesModelProfiles916Schema}
        defaultProps={{ sparkLine: 'The method tracks something real.' }} />
      <Composition id="ValuesSplitScreen916" component={ValuesSplitScreen916}
        durationInFrames={300} fps={30} width={1080} height={1920}
        schema={valuesSplitScreen916Schema}
        defaultProps={{ sparkLine: 'Measurable, not random noise.' }} />
      {/* ── portrait 916 shared components ── */}
      <Composition id="ClaudeTitleOutro916" component={ClaudeTitleOutro916}
        durationInFrames={180} fps={30} width={1080} height={1920}
        schema={claudeTitleOutro916Schema}
        defaultProps={claudeTitleOutro916Schema.parse({})} />
      <Composition id="ClaudeWindow916" component={ClaudeWindow916}
        durationInFrames={360} fps={30} width={1080} height={1920}
        schema={claudeWindow916Schema}
        defaultProps={{
          view: 'artifact',
          artifactTitle: 'Verdict',
          artifactHeading: 'The verdict',
          artifactLines: ['Evidence line one.', 'Evidence line two.'],
          sparkLine: 'Control, not cure.',
        }} />
      <Composition
        id="LogoOutro916"
        component={LogoOutro}
        durationInFrames={120}
        fps={30}
        width={1080}
        height={1920}
        schema={logoOutroSchema}
        defaultProps={{
          svgFile: 'logo-outro/bear-brown/bear-brown-logo-1.svg',
          animation: 'springEntrance' as const,
          durationS: 4,
          aspect: '9:16' as const,
          aspectRatio: 1.5,
          bg: '#FAF9F5',
          accent: '#D97757',
          fill: '#000000',
          paths: '',
          viewBox: '',
          handle: '',
        }}
        calculateMetadata={({props}) => ({
          durationInFrames: Math.max(1, Math.round(props.durationS * 30)),
          width: 1080,
          height: 1920,
        })}
      />
      {/* ── concept-illustration library (STRUCTURAL family) — starter templates ── */}
      <Composition id="Illu-LayerStack" component={LayerStackPreview} durationInFrames={150} fps={30} width={1280} height={720} />
      <Composition id="Illu-SourceFlow" component={SourceFlowPreview} durationInFrames={180} fps={30} width={1280} height={720} />
      <Composition id="Illu-ChipGrid" component={ChipGridPreview} durationInFrames={150} fps={30} width={1280} height={720} />
      <Composition id="Illu-PredictCard" component={PredictCardPreview} durationInFrames={150} fps={30} width={1280} height={720} />
      {/* ── claude-liam-claude-science — structural illustrations (parameterized) ── */}
      <Composition id="ClaudeScienceLayerStack" component={ClaudeScienceLayerStack}
        durationInFrames={900} fps={30} width={1280} height={720}
        schema={claudeScienceLayerStackSchema}
        defaultProps={claudeScienceLayerStackSchema.parse({})} />
      <Composition id="ClaudeScienceSourceFlow" component={ClaudeScienceSourceFlow}
        durationInFrames={900} fps={30} width={1280} height={720}
        schema={claudeScienceSourceFlowSchema}
        defaultProps={claudeScienceSourceFlowSchema.parse({})} />
      <Composition id="ClaudeScienceChipGrid" component={ClaudeScienceChipGrid}
        durationInFrames={900} fps={30} width={1280} height={720}
        schema={claudeScienceChipGridSchema}
        defaultProps={claudeScienceChipGridSchema.parse({})} />
      {/* ── claude-liam-claude-science — rhetorical patterns (deckPatterns, responsive) ── */}
      <Composition id="AttritionChain" component={AttritionChain}
        durationInFrames={900} fps={30} width={1280} height={720}
        defaultProps={{data: {title: '', slideMeta: '', total: 20, startLabel: 'Start', stages: [{label: 'Stage', survival: 0.5}]}}} />
      <Composition id="ScaleComparison" component={ScaleComparison}
        durationInFrames={900} fps={30} width={1280} height={720}
        defaultProps={{data: {slideMeta: '', axis: {min: 1, max: 100, unit: 'yrs'}, band: {from: 5, to: 10, label: 'AI window'}, items: [{label: 'Baseline', value: 50}]}}} />
      <Composition id="DivergentFates" component={DivergentFates}
        durationInFrames={900} fps={30} width={1280} height={720}
        defaultProps={{data: {slideMeta: '', startLabel: 'Start', splitLabel: 'Split', tracks: [{label: 'Track A', outcome: 'Up', tone: 'good', path: 'up', notes: []}, {label: 'Track B', outcome: 'Down', tone: 'warn', path: 'down', notes: []}]}}} />
      <Composition id="BinaryBranch" component={BinaryBranch}
        durationInFrames={900} fps={30} width={1280} height={720}
        defaultProps={{data: {slideMeta: '', question: 'Which path?', branches: [{label: 'A', detail: '', fix: '', tone: 'good'}, {label: 'B', detail: '', fix: '', tone: 'warn'}], resolver: {label: 'Resolver', detail: ''}}}} />
      {/* ── claude-liam — H logo remotion technique showcase (9:16 portrait) ── */}
      <Composition
        id="HLogoRemotionShowcase"
        component={HLogoRemotionShowcase}
        durationInFrames={HLogoRemotionShowcase_FRAMES}
        fps={30}
        width={1080}
        height={1920}
      />
      {/* ── claude-liam — H logo remotion technique showcase (16:9 landscape) ── */}
      <Composition
        id="HLogoRemotionShowcase169"
        component={HLogoRemotionShowcase169}
        durationInFrames={HLogoRemotionShowcase169_FRAMES}
        fps={30}
        width={1920}
        height={1080}
      />
      {/* ── claude-liam — HAI wordmark remotion technique showcase (9:16 portrait) ── */}
      <Composition
        id="HaiWordmarkShowcase"
        component={HaiWordmarkShowcase}
        durationInFrames={HaiWordmarkShowcase_FRAMES}
        fps={30}
        width={1080}
        height={1920}
      />
      {/* ── claude-liam — HAI wordmark remotion technique showcase (16:9 landscape) ── */}
      <Composition
        id="HaiWordmarkShowcase16x9"
        component={HaiWordmarkShowcase16x9}
        durationInFrames={HaiWordmarkShowcase16x9_FRAMES}
        fps={30}
        width={1920}
        height={1080}
      />
      {/* ── claude-liam — Musinique logo-2 remotion technique showcase (16:9 landscape) ── */}
      <Composition
        id="MusiniqueLogo2RemotionShowcase16x9"
        component={MusiniqueLogo2RemotionShowcase16x9}
        durationInFrames={MusiniqueLogo2Showcase16x9_FRAMES}
        fps={30}
        width={1920}
        height={1080}
      />
      {/* ── claude-liam — Musinique logo remotion technique showcase (9:16 portrait) ── */}
      <Composition
        id="MusiniquLogoRemotionShowcase"
        component={MusiniquLogoRemotionShowcase}
        durationInFrames={MusiniquLogoShowcase_FRAMES}
        fps={30}
        width={1080}
        height={1920}
      />
      {/* ── claude-liam — Musinique logo-2 remotion technique showcase (9:16 portrait, 20 techniques) ── */}
      <Composition
        id="MusiniqueLogo2RemotionShowcase"
        component={MusiniqueLogo2RemotionShowcase}
        durationInFrames={MusiniqueLogo2ShowcasePortrait_FRAMES}
        fps={30}
        width={1080}
        height={1920}
      />
      {/* ── claude-liam — Bear Brown initials remotion technique showcase (9:16 portrait) ── */}
      <Composition
        id="BearBrownInitialsShowcase"
        component={BearBrownInitialsShowcase}
        durationInFrames={BearBrownInitialsShowcase_FRAMES}
        fps={30}
        width={1080}
        height={1920}
      />
      {/* ── claude-liam — Bear Brown initials remotion technique showcase (16:9 landscape) ── */}
      <Composition
        id="BearBrownInitialsShowcase169"
        component={BearBrownInitialsShowcase169}
        durationInFrames={BearBrownInitialsShowcase169_FRAMES}
        fps={30}
        width={1920}
        height={1080}
      />
      {/* ── claude-liam — Bear Brown full logo remotion technique showcase (9:16 portrait) ── */}
      <Composition
        id="BearBrownLogoRemotionShowcase"
        component={BearBrownLogoRemotionShowcase}
        durationInFrames={BearBrownLogoShowcase_FRAMES}
        fps={30}
        width={1080}
        height={1920}
      />
      {/* ── claude-liam — Bear Brown full logo remotion technique showcase (16:9 landscape) ── */}
      <Composition
        id="BearBrownLogoRemotionShowcase16x9"
        component={BearBrownLogoRemotionShowcase16x9}
        durationInFrames={BearBrownLogoRemotionShowcase16x9_FRAMES}
        fps={30}
        width={1920}
        height={1080}
      />
      {/* ── claude-liam — Musinique logo remotion technique showcase (16:9 landscape, 20 techniques) ── */}
      <Composition
        id="MusiniquLogoShowcase169"
        component={MusiniquLogoShowcase169}
        durationInFrames={TOTAL_FRAMES_MUSINIQUE}
        fps={30}
        width={1920}
        height={1080}
      />
      {/* ── logo skill — brand sting outro; duration + canvas derived from props ── */}
      <Composition
        id="LogoOutro"
        component={LogoOutro}
        durationInFrames={120}
        fps={30}
        width={1920}
        height={1080}
        schema={logoOutroSchema}
        defaultProps={{
          svgFile: 'logo-outro/bear-brown/bear-brown-logo-1.svg',
          animation: 'springEntrance' as const,
          durationS: 4,
          aspect: '16:9' as const,
          aspectRatio: 1.5,
          bg: '#FAF9F5',
          accent: '#D97757',
          fill: '#000000',
          paths: '',
          viewBox: '',
          handle: '',
        }}
        calculateMetadata={({props}) => ({
          durationInFrames: Math.max(1, Math.round(props.durationS * 30)),
          width: props.aspect === '9:16' ? 1080 : 1920,
          height: props.aspect === '9:16' ? 1920 : 1080,
        })}
      />
      {/* ── claude-liam — algorithmic-art figures ── */}
      <Composition id="AlgArtPipeline" component={AlgArtPipeline}
        durationInFrames={660} fps={30} width={1920} height={1080}
        schema={algArtPipelineSchema}
        defaultProps={{ sparkLine: 'The handoff is the invention.' }} />
      <Composition id="AlgArtOrganicTurbulence" component={AlgArtOrganicTurbulence}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={algArtOrganicTurbulenceSchema}
        defaultProps={{ sparkLine: 'Order from disorder.', showTitle: true }} />
      <Composition id="AlgArtMovementGallery" component={AlgArtMovementGallery}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={algArtMovementGallerySchema}
        defaultProps={{ sparkLine: 'A movement, named.' }} />
      <Composition id="AlgArtHiddenSeed" component={AlgArtHiddenSeed}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={algArtHiddenSeedSchema}
        defaultProps={{ sparkLine: 'Only those who know.' }} />
      <Composition id="AlgArtSeedGrid" component={AlgArtSeedGrid}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={algArtSeedGridSchema}
        defaultProps={{ sparkLine: 'The plate. The print.', highlightSeed: 3 }} />
      <Composition id="AlgArtFixedVariable" component={AlgArtFixedVariable}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={algArtFixedVariableSchema}
        defaultProps={{ sparkLine: 'Fixed outside. Free inside.' }} />
      <Composition id="AlgArtQualityDial" component={AlgArtQualityDial}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={algArtQualityDialSchema}
        defaultProps={{ sparkLine: 'Framing the register.' }} />
      {/* ── claude-liam — agent-development (claude-code) skill teardown figures ── */}
      <Composition id="AgentDevAnatomy" component={AgentDevAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={agentDevAnatomySchema}
        defaultProps={{ sparkLine: 'Frontmatter triggers. Body becomes the system prompt.' }} />
      <Composition id="AgentDevDescription" component={AgentDevDescription}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={agentDevDescriptionSchema}
        defaultProps={{ sparkLine: 'Examples teach triggering. No examples, no trigger.' }} />
      <Composition id="AgentDevTell" component={AgentDevTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={agentDevTellSchema}
        defaultProps={{ sparkLine: 'Description field nailed. Decision tree missing.' }} />
      {/* ── claude-liam — sentry-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="SentryApiAnatomy" component={SentryApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={sentryApiAnatomySchema}
        defaultProps={{ sparkLine: 'Org → project → issue (group) → event. sentry_issues.sh pages Link-header cursors. frames[-1] = crash.' }} />
      <Composition id="SentryApiDesign" component={SentryApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={sentryApiDesignSchema}
        defaultProps={{ sparkLine: 'Resolve shortId first. Link-header cursors. Check detail on PUT. -L for trailing-slash redirects.' }} />
      <Composition id="SentryApiTell" component={SentryApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={sentryApiTellSchema}
        defaultProps={{ sparkLine: 'Security note + sentry_issues.sh + shortId + frame order + rate-limit header correct. Trailing slash + PUT detail bite.' }} />
      {/* ── claude-liam — salesforce-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="SalesforceApiAnatomy" component={SalesforceApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={salesforceApiAnatomySchema}
        defaultProps={{ sparkLine: 'Per-org instance URL + versioned path. Errors = JSON array. sf_query.sh pages nextRecordsUrl.' }} />
      <Composition id="SalesforceApiDesign" component={SalesforceApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={salesforceApiDesignSchema}
        defaultProps={{ sparkLine: 'Guard jq with type check. Describe before field names. PATCH/DELETE = 204. nextRecordsUrl not OFFSET.' }} />
      <Composition id="SalesforceApiTell" component={SalesforceApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={salesforceApiTellSchema}
        defaultProps={{ sparkLine: 'sf_query.sh pagination + error-array guard + upsert 300 + composite caveat correct. PATCH 204 + SOSL -G bite.' }} />
      {/* ── claude-liam — redshift-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="RedshiftApiAnatomy" component={RedshiftApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={redshiftApiAnatomySchema}
        defaultProps={{ sparkLine: 'POST only, no REST paths. Region + RS_TARGET required. rs_query.sh drives the async loop.' }} />
      <Composition id="RedshiftApiDesign" component={RedshiftApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={redshiftApiDesignSchema}
        defaultProps={{ sparkLine: 'Poll before read. Decode typed cells. 3 TPS catalog cap. Sub-statement IDs for batch results.' }} />
      <Composition id="RedshiftApiTell" component={RedshiftApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={redshiftApiTellSchema}
        defaultProps={{ sparkLine: 'rs_query.sh + three connection modes + error envelope + rate limits correct. Idempotency + sub-statement fetch bite.' }} />
      {/* ── claude-liam — project-artifact (claude-plugins-official) skill teardown figures ── */}
      <Composition id="ProjectArtifactAnatomy" component={ProjectArtifactAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={projectArtifactAnatomySchema}
        defaultProps={{ sparkLine: 'Overview + Workstreams always. Five conditional tabs earn their place. State block enables delta refresh.' }} />
      <Composition id="ProjectArtifactDesign" component={ProjectArtifactDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={projectArtifactDesignSchema}
        defaultProps={{ sparkLine: 'Gather live sources first. Pick tabs before HTML. Embed state block always. Delta on refresh.' }} />
      <Composition id="ProjectArtifactTell" component={ProjectArtifactTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={projectArtifactTellSchema}
        defaultProps={{ sparkLine: 'Tab catalog + state block + freshness + entity-encoding correct. Machine-local config + delta prerequisite bite.' }} />
      {/* ── claude-liam — playground (claude-plugins-official) skill teardown figures ── */}
      <Composition id="PlaygroundAnatomy" component={PlaygroundAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={playgroundAnatomySchema}
        defaultProps={{ sparkLine: 'Six templates, four zones. Single HTML file, live preview, natural-language prompt, presets.' }} />
      <Composition id="PlaygroundDesign" component={PlaygroundDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={playgroundDesignSchema}
        defaultProps={{ sparkLine: 'Identify type. State pattern from the start. Natural-language prompt. Open in browser to verify.' }} />
      <Composition id="PlaygroundTell" component={PlaygroundTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={playgroundTellSchema}
        defaultProps={{ sparkLine: 'Templates + state pattern + anti-value-dump rule correct. No starter HTML; dark theme unspecified.' }} />
      {/* ── claude-liam — pagerduty-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="PagerdutyApiAnatomy" component={PagerdutyApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={pagerdutyApiAnatomySchema}
        defaultProps={{ sparkLine: 'Two hosts, two auth models. Alert → service → policy → schedule → incident. Log entries = paged-why.' }} />
      <Composition id="PagerdutyApiDesign" component={PagerdutyApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={pagerdutyApiDesignSchema}
        defaultProps={{ sparkLine: 'Sanity check first. Trace routing before incidents. Log entries for paged-why. From: on every mutation.' }} />
      <Composition id="PagerdutyApiTell" component={PagerdutyApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={pagerdutyApiTellSchema}
        defaultProps={{ sparkLine: 'Two-API split + 401 empty body + pd_oncall.sh + rate limits correct. curl -g + From: + type field bite.' }} />
      {/* ── claude-liam — notion-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="NotionApiAnatomy" component={NotionApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={notionApiAnatomySchema}
        defaultProps={{ sparkLine: 'Page = block. DB → data source → schema. Data source ID ≠ DB ID. 404 = sharing, not bad ID.' }} />
      <Composition id="NotionApiDesign" component={NotionApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={notionApiDesignSchema}
        defaultProps={{ sparkLine: 'Sanity check first. DB → data source ID. Schema before filter. Sharing before debugging 404.' }} />
      <Composition id="NotionApiTell" component={NotionApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={notionApiTellSchema}
        defaultProps={{ sparkLine: 'Scripts + content model + data-source ID distinction correct. Child recursion missing; file URLs expire.' }} />
      {/* ── claude-liam — mcp-integration (claude-plugins-official) skill teardown figures ── */}
      <Composition id="McpIntegrationAnatomy" component={McpIntegrationAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={mcpIntegrationAnatomySchema}
        defaultProps={{ sparkLine: 'stdio local process. SSE OAuth cloud. HTTP token REST. WebSocket real-time. Lazy load. Restart on config change.' }} />
      <Composition id="McpIntegrationDesign" component={McpIntegrationDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={mcpIntegrationDesignSchema}
        defaultProps={{ sparkLine: '.mcp.json separation. ${CLAUDE_PLUGIN_ROOT} for paths. Pre-allow specifics via /mcp. Document env vars.' }} />
      <Composition id="McpIntegrationTell" component={McpIntegrationTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={mcpIntegrationTellSchema}
        defaultProps={{ sparkLine: 'Four types, OAuth automatic, portable paths correct. Tool name fragile; no live reload; wildcard bypasses permissions.' }} />
      {/* ── claude-liam — math-olympiad (claude-plugins-official) skill teardown figures ── */}
      <Composition id="MathOlympiadAnatomy" component={MathOlympiadAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={mathOlympiadAnatomySchema}
        defaultProps={{ sparkLine: 'Interpretation check. Strip thinking trace. Pattern-armed attack. Asymmetric vote. Abstain honestly.' }} />
      <Composition id="MathOlympiadDesign" component={MathOlympiadDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={mathOlympiadDesignSchema}
        defaultProps={{ sparkLine: 'Check interpretation. Label every agent. Deep mode before abstain. Presentation is separate from correctness.' }} />
      <Composition id="MathOlympiadTell" component={MathOlympiadTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={mathOlympiadTellSchema}
        defaultProps={{ sparkLine: 'Dual isolation and asymmetric vote correct. VERBATIM enforcement fragile; pattern files must be loaded.' }} />
      {/* ── claude-liam — m5-onboard (claude-plugins-official) skill teardown figures ── */}
      <Composition id="M5OnboardAnatomy" component={M5OnboardAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={m5OnboardAnatomySchema}
        defaultProps={{ sparkLine: 'One orchestrator: detect, identify, flash, install. Button dance blocks the flash stage.' }} />
      <Composition id="M5OnboardDesign" component={M5OnboardDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={m5OnboardDesignSchema}
        defaultProps={{ sparkLine: 'Ask variant first. Background + tee. Relay button dance. Install-only mode for already-flashed.' }} />
      <Composition id="M5OnboardTell" component={M5OnboardTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={m5OnboardTellSchema}
        defaultProps={{ sparkLine: 'Button dance and background run pattern correct. NVS blob bug and dialout group buried.' }} />
      {/* ── claude-liam — linear-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="LinearApiAnatomy" component={LinearApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={linearApiAnatomySchema}
        defaultProps={{ sparkLine: 'One endpoint. UUID for mutations. No Bearer prefix. HTTP 200 can mean failure.' }} />
      <Composition id="LinearApiDesign" component={LinearApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={linearApiDesignSchema}
        defaultProps={{ sparkLine: 'UUID before mutate. Markdown body. Rate limit is HTTP 400 not 429. Epoch milliseconds.' }} />
      <Composition id="LinearApiTell" component={LinearApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={linearApiTellSchema}
        defaultProps={{ sparkLine: 'No-REST note and HTTP-200-on-error correct. Rate limit HTTP 400 easy to miss in retry logic.' }} />
      {/* ── claude-liam — jira-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="JiraApiAnatomy" component={JiraApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={jiraApiAnatomySchema}
        defaultProps={{ sparkLine: 'v3 for issues. ADF for body text. Transitions by ID. Three pagination schemes.' }} />
      <Composition id="JiraApiDesign" component={JiraApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={jiraApiDesignSchema}
        defaultProps={{ sparkLine: 'Sanity check. createmeta before create. Bounded JQL. accountId not email.' }} />
      <Composition id="JiraApiTell" component={JiraApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={jiraApiTellSchema}
        defaultProps={{ sparkLine: 'ADF and transition workflow correct. Three pagination schemes with no detection guide.' }} />
      {/* ── claude-liam — hubspot-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="HubSpotApiAnatomy" component={HubSpotApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={hubSpotApiAnatomySchema}
        defaultProps={{ sparkLine: 'Uniform v3 path. Properties opt-in. Dedup by email/domain. Search capped at 10,000.' }} />
      <Composition id="HubSpotApiDesign" component={HubSpotApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={hubSpotApiDesignSchema}
        defaultProps={{ sparkLine: 'Sanity check first. Discover schema before write. properties= on every read. Batch for bulk.' }} />
      <Composition id="HubSpotApiTell" component={HubSpotApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={hubSpotApiTellSchema}
        defaultProps={{ sparkLine: 'Uniform model and properties= contract both correct. Default property set deferred to references/api.md.' }} />
      {/* ── claude-liam — hook-development (claude-plugins-official) skill teardown figures ── */}
      <Composition id="HookDevelopmentAnatomy" component={HookDevelopmentAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={hookDevelopmentAnatomySchema}
        defaultProps={{ sparkLine: 'Prompt-Based for judgment. Command for determinism. CLAUDE_PLUGIN_ROOT for portability.' }} />
      <Composition id="HookDevelopmentDesign" component={HookDevelopmentDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={hookDevelopmentDesignSchema}
        defaultProps={{ sparkLine: '9 events. 4 support prompt hooks. All hooks run in parallel — no ordering.' }} />
      <Composition id="HookDevelopmentTell" component={HookDevelopmentTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={hookDevelopmentTellSchema}
        defaultProps={{ sparkLine: 'Prompt hooks are right for judgment. But they only fire on 4 of 9 events — unstated.' }} />
      {/* ── claude-liam — graphing (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="GraphingAnatomy" component={GraphingAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={graphingAnatomySchema}
        defaultProps={{ sparkLine: 'theme() derives colors from luminance. write_html inlines offline. zero_fill_days: skip if zeros would lie.' }} />
      <Composition id="GraphingDesign" component={GraphingDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={graphingDesignSchema}
        defaultProps={{ sparkLine: 'Four steps: look, infer, write, look again. Rank bars. Label small datasets. Annotate what matters.' }} />
      <Composition id="GraphingTell" component={GraphingTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={graphingTellSchema}
        defaultProps={{ sparkLine: 'Judgement-first workflow and offline write_html correct. GRID/ACCENT placeholders must be substituted manually.' }} />
      {/* ── claude-liam — grafana-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="GrafanaApiAnatomy" component={GrafanaApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={grafanaApiAnatomySchema}
        defaultProps={{ sparkLine: 'Three time formats. Same API, different base URL. Datasource error in results.<refId>.error, not status.' }} />
      <Composition id="GrafanaApiDesign" component={GrafanaApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={grafanaApiDesignSchema}
        defaultProps={{ sparkLine: 'Two alert surfaces: live state vs definitions. Dashboard update = full replace. Batch queries[], not loops.' }} />
      <Composition id="GrafanaApiTell" component={GrafanaApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={grafanaApiTellSchema}
        defaultProps={{ sparkLine: 'Time units and alert surfaces separated cleanly. grafana() helper session-only; GNU/BSD date gap.' }} />
      {/* ── claude-liam — google-drive-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="GoogleDriveApiAnatomy" component={GoogleDriveApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={googleDriveApiAnatomySchema}
        defaultProps={{ sparkLine: 'Everything is a file. Workspace files have no bytes. fields= or nextPageToken silently vanishes.' }} />
      <Composition id="GoogleDriveApiDesign" component={GoogleDriveApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={googleDriveApiDesignSchema}
        defaultProps={{ sparkLine: 'fields= silently drops nextPageToken. Workspace files: export path, not alt=media. Shared drive 404 = missing param.' }} />
      <Composition id="GoogleDriveApiTell" component={GoogleDriveApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={googleDriveApiTellSchema}
        defaultProps={{ sparkLine: 'Two-host model and Workspace no-bytes trap nailed. fields= nextPageToken gap: easy to miss.' }} />
      {/* ── claude-liam — example-skill (claude-plugins-official) skill teardown figures ── */}
      <Composition id="ExampleSkillAnatomy" component={ExampleSkillAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={exampleSkillAnatomySchema}
        defaultProps={{ sparkLine: 'Description is the trigger. Required: name + description. Optional: version, license, subdirectories.' }} />
      <Composition id="ExampleSkillDesign" component={ExampleSkillDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={exampleSkillDesignSchema}
        defaultProps={{ sparkLine: 'Description triggers model judgment. Three modes: skill vs command vs agent. Overlap: no detection method.' }} />
      <Composition id="ExampleSkillTell" component={ExampleSkillTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={exampleSkillTellSchema}
        defaultProps={{ sparkLine: 'Three-mode distinction and description trigger solid. Trigger mechanism and testing: unspecified.' }} />
      {/* ── claude-liam — example-command (claude-plugins-official) skill teardown figures ── */}
      <Composition id="ExampleCommandAnatomy" component={ExampleCommandAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={exampleCommandAnatomySchema}
        defaultProps={{ sparkLine: 'Five frontmatter fields. $ARGUMENTS injection. Same loading as legacy commands/ format.' }} />
      <Composition id="ExampleCommandDesign" component={ExampleCommandDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={exampleCommandDesignSchema}
        defaultProps={{ sparkLine: 'Format reference, not a demo. Allowed-tools: pre-approved but unscoped in the template.' }} />
      <Composition id="ExampleCommandTell" component={ExampleCommandTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={exampleCommandTellSchema}
        defaultProps={{ sparkLine: 'Schema complete and $ARGUMENTS visible. Bash blast radius and $ARGUMENTS parsing: not shown.' }} />
      {/* ── claude-liam — enterprise-search (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="EnterpriseSearchAnatomy" component={EnterpriseSearchAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={enterpriseSearchAnatomySchema}
        defaultProps={{ sparkLine: 'Search → read → feedback. Index first, always. Two scripts for the hot path.' }} />
      <Composition id="EnterpriseSearchDesign" component={EnterpriseSearchDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={enterpriseSearchDesignSchema}
        defaultProps={{ sparkLine: 'Cursor pagination. Broaden before giving up. Feedback trains the ranker — both labels.' }} />
      <Composition id="EnterpriseSearchTell" component={EnterpriseSearchTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={enterpriseSearchTellSchema}
        defaultProps={{ sparkLine: 'Three-step loop and bundled scripts solid. Feedback has no script and negatives will get skipped.' }} />
      {/* ── claude-liam — debug-plugins (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="DebugPluginsAnatomy" component={DebugPluginsAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={debugPluginsAnatomySchema}
        defaultProps={{ sparkLine: 'Six steps in order. Collect all findings before reporting.' }} />
      <Composition id="DebugPluginsDesign" component={DebugPluginsDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={debugPluginsDesignSchema}
        defaultProps={{ sparkLine: 'Session snapshot on start. Config changes: fresh thread only. Stdout gap: structured errors invisible.' }} />
      <Composition id="DebugPluginsTell" component={DebugPluginsTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={debugPluginsTellSchema}
        defaultProps={{ sparkLine: 'Ladder and security note solid. Stdout gap and unzip Bash tension: surface them.' }} />
      {/* ── claude-liam — datadog-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="DatadogApiAnatomy" component={DatadogApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={datadogApiAnatomySchema}
        defaultProps={{ sparkLine: 'v1 or v2 by resource, not generation. Regional site first.' }} />
      <Composition id="DatadogApiDesign" component={DatadogApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={datadogApiDesignSchema}
        defaultProps={{ sparkLine: 'Three pagination schemes. Spans vs logs: different JSON:API depth.' }} />
      <Composition id="DatadogApiTell" component={DatadogApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={datadogApiTellSchema}
        defaultProps={{ sparkLine: 'Site check, v1/v2 routing, and pagination solid. Spans envelope and dashboard PUT trap: surface them.' }} />
      {/* ── claude-liam — confluence-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="ConfluenceApiAnatomy" component={ConfluenceApiAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={confluenceApiAnatomySchema}
        defaultProps={{ sparkLine: 'v2 by default. v1 only for search, upload, labels.' }} />
      <Composition id="ConfluenceApiDesign" component={ConfluenceApiDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={confluenceApiDesignSchema}
        defaultProps={{ sparkLine: 'Prompt injection: first note. Pagination: different base for v1 and v2.' }} />
      <Composition id="ConfluenceApiTell" component={ConfluenceApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={confluenceApiTellSchema}
        defaultProps={{ sparkLine: 'Pagination trap and security note solid. /wiki warning buried and atlas_doc_format gap: surface them.' }} />
      {/* ── claude-liam — configure (claude-plugins-official discord) skill teardown figures ── */}
      <Composition id="ConfigureAnatomy" component={ConfigureAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={configureAnatomySchema}
        defaultProps={{ sparkLine: 'Three modes. Two files. Different restart rules for each.' }} />
      <Composition id="ConfigureDesign" component={ConfigureDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={configureDesignSchema}
        defaultProps={{ sparkLine: 'Pairing captures IDs. Allowlist locks them. Close the loop.' }} />
      <Composition id="ConfigureTell" component={ConfigureTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={configureTellSchema}
        defaultProps={{ sparkLine: 'Lockdown rule and credential hygiene solid. Token validation and schema gaps: surface them.' }} />
      {/* ── claude-liam — config-guide (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="ConfigGuideAnatomy" component={ConfigGuideAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={configGuideAnatomySchema}
        defaultProps={{ sparkLine: 'Four layers. Five reference files. Always verify with debug-plugins.' }} />
      <Composition id="ConfigGuideDesign" component={ConfigGuideDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={configGuideDesignSchema}
        defaultProps={{ sparkLine: 'Index routes. Each reference self-contained. Slack only — caveat up front.' }} />
      <Composition id="ConfigGuideTell" component={ConfigGuideTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={configGuideTellSchema}
        defaultProps={{ sparkLine: 'Four-layer model and index pattern solid. Silent-failure risk and Slack-only gap: surface them.' }} />
      {/* ── claude-liam — claude-opus-4-5-migration (claude-code) skill teardown figures ── */}
      <Composition id="Opus45MigrationMatrix" component={Opus45MigrationMatrix}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={opus45MigrationMatrixSchema}
        defaultProps={{ sparkLine: 'Four platforms. Three source models. One beta header to remove.' }} />
      <Composition id="Opus45MigrationTriggers" component={Opus45MigrationTriggers}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={opus45MigrationTriggersSchema}
        defaultProps={{ sparkLine: 'Opt-in only. Apply if reported. Never apply by default.' }} />
      <Composition id="Opus45MigrationTell" component={Opus45MigrationTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={opus45MigrationTellSchema}
        defaultProps={{ sparkLine: 'Platform matrix and opt-in discipline solid. Azure gap and vague triggers: surface them.' }} />
      {/* ── claude-liam — claude-md-improver (claude-plugins-official) skill teardown figures ── */}
      <Composition id="ClaudeMdImproverLocations" component={ClaudeMdImproverLocations}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={claudeMdImproverLocationsSchema}
        defaultProps={{ sparkLine: 'Five locations. Six criteria. Score before you touch.' }} />
      <Composition id="ClaudeMdImproverWorkflow" component={ClaudeMdImproverWorkflow}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={claudeMdImproverWorkflowSchema}
        defaultProps={{ sparkLine: 'Report first. Diff-with-why. Minimal additions only.' }} />
      <Composition id="ClaudeMdImproverTell" component={ClaudeMdImproverTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={claudeMdImproverTellSchema}
        defaultProps={{ sparkLine: 'Report gate and diff-with-why solid. head-50 cap and unattended gap: surface them.' }} />
      {/* ── claude-liam — claude-automation-recommender (claude-plugins-official) skill teardown figures ── */}
      <Composition id="AutomationRecommenderTypes" component={AutomationRecommenderTypes}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={automationRecommenderTypesSchema}
        defaultProps={{ sparkLine: 'Five types. Hooks automatic. Subagents parallel. Skills deliberate. Plugins bundle. MCP external.' }} />
      <Composition id="AutomationRecommenderSignals" component={AutomationRecommenderSignals}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={automationRecommenderSignalsSchema}
        defaultProps={{ sparkLine: 'Detect signals. Match type. Cap at 1-2. Tell users they can ask for more.' }} />
      <Composition id="AutomationRecommenderTell" component={AutomationRecommenderTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={automationRecommenderTellSchema}
        defaultProps={{ sparkLine: 'Five-type taxonomy and 1-2 discipline solid. Reference-file escape and monorepo gap: surface them.' }} />
      {/* ── claude-liam — cardputer-buddy (claude-plugins-official) skill teardown figures ── */}
      <Composition id="CardputerBuddyLayout" component={CardputerBuddyLayout}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={cardputerBuddyLayoutSchema}
        defaultProps={{ sparkLine: 'Drop a .py in apps/. Push it. Appears on next boot. No registration needed.' }} />
      <Composition id="CardputerBuddyScripts" component={CardputerBuddyScripts}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={cardputerBuddyScriptsSchema}
        defaultProps={{ sparkLine: 'install_apps for full sync. push for one file. tail to watch. repl for one-shot probes.' }} />
      <Composition id="CardputerBuddyTell" component={CardputerBuddyTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={cardputerBuddyTellSchema}
        defaultProps={{ sparkLine: 'Layout and dev-loop scripts solid. PORT gap and push-script ambiguity: surface them.' }} />
      {/* ── claude-liam — build-mcpb (claude-plugins-official) skill teardown figures ── */}
      <Composition id="BuildMcpbAnatomy" component={BuildMcpbAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={buildMcpbAnatomySchema}
        defaultProps={{ sparkLine: 'Zip archive. mcp_config is the launch. No auto-prefix on env vars.' }} />
      <Composition id="BuildMcpbPipeline" component={BuildMcpbPipeline}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={buildMcpbPipelineSchema}
        defaultProps={{ sparkLine: 'Local machine only. No sandbox. Test without your toolchain before shipping.' }} />
      <Composition id="BuildMcpbTell" component={BuildMcpbTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={buildMcpbTellSchema}
        defaultProps={{ sparkLine: 'MCPB gate and no-sandbox warning solid. Env var no-prefix trap: surface it at the manifest.' }} />
      {/* ── claude-liam — build-mcp-server (claude-plugins-official) skill teardown figures ── */}
      <Composition id="BuildMcpServerDeployment" component={BuildMcpServerDeployment}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={buildMcpServerDeploymentSchema}
        defaultProps={{ sparkLine: 'Remote HTTP default. MCPB for local. stdio for prototypes only.' }} />
      <Composition id="BuildMcpServerPatterns" component={BuildMcpServerPatterns}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={buildMcpServerPatternsSchema}
        defaultProps={{ sparkLine: 'Under 15 tools: one per action. Large surface: search+execute. Most servers only need tools.' }} />
      <Composition id="BuildMcpServerTell" component={BuildMcpServerTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={buildMcpServerTellSchema}
        defaultProps={{ sparkLine: 'Discovery-before-code and remote-HTTP default solid. Elicitation check and FastMCP split: surface them.' }} />
      {/* ── claude-liam — build-mcp-app (claude-plugins-official) skill teardown figures ── */}
      <Composition id="BuildMcpAppAnatomy" component={BuildMcpAppAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={buildMcpAppAnatomySchema}
        defaultProps={{ sparkLine: 'Tool returns data. Resource serves HTML. App bridges them. Bundle must be inlined.' }} />
      <Composition id="BuildMcpAppDecision" component={BuildMcpAppDecision}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={buildMcpAppDecisionSchema}
        defaultProps={{ sparkLine: 'Elicitation first. Widget for searchable lists, visuals, live progress. Text if none apply.' }} />
      <Composition id="BuildMcpAppTell" component={BuildMcpAppTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={buildMcpAppTellSchema}
        defaultProps={{ sparkLine: 'Two-part reg and bundle-inlining documented. Cache flush and CSP blank: surface them earlier.' }} />
      {/* ── claude-liam — bigquery-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="BigQueryApiAnatomy" component={BigQueryApiAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={bigQueryApiAnatomySchema}
        defaultProps={{ sparkLine: 'Job owns the query. Billing project pays. Location pins the job. DONE ≠ success.' }} />
      <Composition id="BigQueryApiOps" component={BigQueryApiOps}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={bigQueryApiOpsSchema}
        defaultProps={{ sparkLine: 'Eight operations. Script drives the hard parts. Preview is free. Direct submit for destination tables.' }} />
      <Composition id="BigQueryApiTell" component={BigQueryApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={bigQueryApiTellSchema}
        defaultProps={{ sparkLine: 'DONE ≠ success and location-always are the two rules. Pagination field split: document it.' }} />
      {/* ── claude-liam — asana-api (claude-tag-plugins) skill teardown figures ── */}
      <Composition id="AsanaApiAnatomy" component={AsanaApiAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={asanaApiAnatomySchema}
        defaultProps={{ sparkLine: 'gid is the key. data is the envelope. opt_fields is the escape hatch.' }} />
      <Composition id="AsanaApiOps" component={AsanaApiOps}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={asanaApiOpsSchema}
        defaultProps={{ sparkLine: 'Ten operations. One script. Pagination handled. gid required before every write.' }} />
      <Composition id="AsanaApiTell" component={AsanaApiTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={asanaApiTellSchema}
        defaultProps={{ sparkLine: 'Three rules land. Search premium cap and references/api.md dependency: document inline.' }} />
      {/* ── claude-liam — agent-development (claude-plugins-official) prose-trigger figures ── */}
      <Composition id="AgentDevTriggerProse" component={AgentDevTriggerProse}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={agentDevTriggerProseSchema}
        defaultProps={{ sparkLine: 'Prose in description. Prose in body. Two locations, two audiences, one maintenance burden.' }} />
      <Composition id="AgentDevTell2" component={AgentDevTell2}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={agentDevTell2Schema}
        defaultProps={{ sparkLine: 'Two-location trigger docs readable. Maintenance coupling: consolidate.' }} />
      {/* ── claude-liam — access (discord plugin) skill teardown figures ── */}
      <Composition id="DiscordAccessAnatomy" component={DiscordAccessAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={discordAccessAnatomySchema}
        defaultProps={{ sparkLine: 'One JSON file. Five fields. Terminal only — channel messages carry injection.' }} />
      <Composition id="DiscordAccessCommands" component={DiscordAccessCommands}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={discordAccessCommandsSchema}
        defaultProps={{ sparkLine: 'Read before write. Never auto-pick pending. approved/ dir is the handshake.' }} />
      <Composition id="DiscordAccessTell" component={DiscordAccessTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={discordAccessTellSchema}
        defaultProps={{ sparkLine: 'Prompt injection defense clear. $ARGUMENTS exposure: document it.' }} />
      {/* ── claude-liam — writing-rules (hookify plugin) skill teardown figures ── */}
      <Composition id="HookifyRuleAnatomy" component={HookifyRuleAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={hookifyRuleAnatomySchema}
        defaultProps={{ sparkLine: 'Name it. Event it. Pattern it. Message it. One markdown file, immediate effect.' }} />
      <Composition id="HookifyEventTypes" component={HookifyEventTypes}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={hookifyEventTypesSchema}
        defaultProps={{ sparkLine: 'bash catches commands. file catches edits. stop catches completion. conditions stack.' }} />
      <Composition id="HookifyTell" component={HookifyTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={hookifyTellSchema}
        defaultProps={{ sparkLine: 'Format solid. Block action and stop/prompt condition fields: document them.' }} />
      {/* ── claude-liam — skill-development (claude-code) skill teardown figures ── */}
      <Composition id="SkillDevAnatomy" component={SkillDevAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={skillDevAnatomySchema}
        defaultProps={{ sparkLine: 'Metadata triggers. Body guides. Resources load as needed. Keep each level lean.' }} />
      <Composition id="SkillDevProcess" component={SkillDevProcess}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={skillDevProcessSchema}
        defaultProps={{ sparkLine: 'Third-person triggers. Imperative body. Lean SKILL.md. Reference everything.' }} />
      <Composition id="SkillDevTell" component={SkillDevTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={skillDevTellSchema}
        defaultProps={{ sparkLine: 'Disclosure model clear. Trigger mechanism: explain how it actually decides.' }} />
      {/* ── claude-liam — plugin-structure (claude-code) skill teardown figures ── */}
      <Composition id="PluginStructureAnatomy" component={PluginStructureAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={pluginStructureAnatomySchema}
        defaultProps={{ sparkLine: 'plugin.json in .claude-plugin/. Components at root. Never inside .claude-plugin/.' }} />
      <Composition id="PluginStructureComponents" component={PluginStructureComponents}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={pluginStructureComponentsSchema}
        defaultProps={{ sparkLine: 'Commands slash. Agents auto. Skills need SKILL.md. Paths need ${CLAUDE_PLUGIN_ROOT}.' }} />
      <Composition id="PluginStructureTell" component={PluginStructureTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={pluginStructureTellSchema}
        defaultProps={{ sparkLine: 'Auto-discovery solid. Placement rule: both silent and fatal.' }} />
      {/* ── claude-liam — plugin-settings (claude-code) skill teardown figures ── */}
      <Composition id="PluginSettingsAnatomy" component={PluginSettingsAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={pluginSettingsAnatomySchema}
        defaultProps={{ sparkLine: 'One file. Three consumers. YAML on top, context below.' }} />
      <Composition id="PluginSettingsPatterns" component={PluginSettingsPatterns}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={pluginSettingsPatternsSchema}
        defaultProps={{ sparkLine: 'Toggle with enabled. Coordinate with body. Parse with sed — carefully.' }} />
      <Composition id="PluginSettingsTell" component={PluginSettingsTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={pluginSettingsTellSchema}
        defaultProps={{ sparkLine: 'Pattern clear. sed parser: bring your own validation.' }} />
      {/* ── claude-liam — mcp-integration (claude-code) skill teardown figures ── */}
      <Composition id="McpIntAnatomy" component={McpIntAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={mcpIntAnatomySchema}
        defaultProps={{ sparkLine: 'stdio spawns. SSE authenticates. HTTP calls. ws streams.' }} />
      <Composition id="McpIntPatterns" component={McpIntPatterns}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={mcpIntPatternsSchema}
        defaultProps={{ sparkLine: 'Tool name is the contract. One underscore wrong: silent failure.' }} />
      <Composition id="McpIntTell" component={McpIntTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={mcpIntTellSchema}
        defaultProps={{ sparkLine: 'Configuration solid. Tool name typo: silent.' }} />
      {/* ── claude-liam — hook-development (claude-code) skill teardown figures ── */}
      <Composition id="HookDevAnatomy" component={HookDevAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={hookDevAnatomySchema}
        defaultProps={{ sparkLine: 'Nine events. Two types. Prompt for judgment, command for speed.' }} />
      <Composition id="HookDevConfig" component={HookDevConfig}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={hookDevConfigSchema}
        defaultProps={{ sparkLine: 'Format mismatch is silent. Parallel hooks cannot coordinate.' }} />
      <Composition id="HookDevTell" component={HookDevTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={hookDevTellSchema}
        defaultProps={{ sparkLine: 'Event model complete. Format mismatch: silent failure.' }} />
      {/* ── claude-liam — command-development (claude-code) skill teardown figures ── */}
      <Composition id="CommandDevAnatomy" component={CommandDevAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={commandDevAnatomySchema}
        defaultProps={{ sparkLine: 'Location sets scope. allowed-tools sets blast radius.' }} />
      <Composition id="CommandDevContent" component={CommandDevContent}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={commandDevContentSchema}
        defaultProps={{ sparkLine: "The body is Claude's directive. Write it that way." }} />
      <Composition id="CommandDevTell" component={CommandDevTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={commandDevTellSchema}
        defaultProps={{ sparkLine: 'Instructions rule solid. Bash detail: bring the reference.' }} />
      {/* ── claude-liam — xlsx skill teardown figures ── */}
      <Composition id="XlsxAnatomy" component={XlsxAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={xlsxAnatomySchema}
        defaultProps={{ sparkLine: 'Tool decision. Six steps. recalc.py is mandatory.' }} />
      <Composition id="XlsxStandards" component={XlsxStandards}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={xlsxStandardsSchema}
        defaultProps={{ sparkLine: 'Blue inputs. Black formulas. Never hardcode a calc.' }} />
      <Composition id="XlsxTell" component={XlsxTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={xlsxTellSchema}
        defaultProps={{ sparkLine: 'Formula mandate solid. data_only trap bites.' }} />
      {/* ── claude-liam — webapp-testing skill teardown figures ── */}
      <Composition id="WebappTestingAnatomy" component={WebappTestingAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={webappTestingAnatomySchema}
        defaultProps={{ sparkLine: 'Static: read → script. Dynamic: server → recon → act.' }} />
      <Composition id="WebappTestingPatterns" component={WebappTestingPatterns}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={webappTestingPatternsSchema}
        defaultProps={{ sparkLine: 'Server managed. Recon first. networkidle always.' }} />
      <Composition id="WebappTestingTell" component={WebappTestingTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={webappTestingTellSchema}
        defaultProps={{ sparkLine: 'Decision tree solid. Error recovery missing.' }} />
      {/* ── claude-liam — web-artifacts-builder skill teardown figures ── */}
      <Composition id="WebArtifactsAnatomy" component={WebArtifactsAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={webArtifactsAnatomySchema}
        defaultProps={{ sparkLine: 'Init once. Develop. Bundle. Share bundle.html.' }} />
      <Composition id="WebArtifactsDesign" component={WebArtifactsDesign}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={webArtifactsDesignSchema}
        defaultProps={{ sparkLine: 'No centered layouts. No purple gradients. No Inter font.' }} />
      <Composition id="WebArtifactsTell" component={WebArtifactsTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={webArtifactsTellSchema}
        defaultProps={{ sparkLine: 'One init. One bundle. One shareable HTML file.' }} />
      {/* ── claude-liam — slack-gif-creator skill teardown figures ── */}
      <Composition id="SlackGifAnatomy" component={SlackGifAnatomy}
        durationInFrames={840} fps={30} width={1920} height={1080}
        schema={slackGifAnatomySchema}
        defaultProps={{ sparkLine: 'Know the spec. Use the toolkit. Write the PIL logic yourself.' }} />
      <Composition id="SlackGifAnimations" component={SlackGifAnimations}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={slackGifAnimationsSchema}
        defaultProps={{ sparkLine: 'Combine concepts. PIL does more than you think.' }} />
      <Composition id="SlackGifTell" component={SlackGifTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={slackGifTellSchema}
        defaultProps={{ sparkLine: 'GIF is a constraint problem. Solve it with PIL primitives.' }} />
      {/* ── claude-liam — skill-creator skill teardown figures ── */}
      <Composition id="SkillCreatorAnatomy" component={SkillCreatorAnatomy}
        durationInFrames={1020} fps={30} width={1920} height={1080}
        schema={skillCreatorAnatomySchema}
        defaultProps={{ sparkLine: 'Draft. Test. Eval. Improve. Repeat.' }} />
      <Composition id="SkillCreatorEvalLoop" component={SkillCreatorEvalLoop}
        durationInFrames={1080} fps={30} width={1920} height={1080}
        schema={skillCreatorEvalLoopSchema}
        defaultProps={{ sparkLine: 'Parallel runs. Quantitative grades. Human review first.' }} />
      <Composition id="SkillCreatorTell" component={SkillCreatorTell}
        durationInFrames={1080} fps={30} width={1920} height={1080}
        schema={skillCreatorTellSchema}
        defaultProps={{ sparkLine: 'A skill is only as good as its eval set.' }} />
      {/* ── claude-liam — pptx skill teardown figures ── */}
      <Composition id="PptxAnatomy" component={PptxAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={pptxAnatomySchema}
        defaultProps={{ sparkLine: 'Read. Edit template. Create scratch. Then QA.' }} />
      <Composition id="PptxDesign" component={PptxDesign}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={pptxDesignSchema}
        defaultProps={{ sparkLine: 'Design for this topic. Not for any topic.' }} />
      <Composition id="PptxTell" component={PptxTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={pptxTellSchema}
        defaultProps={{ sparkLine: 'Design and QA are requirements. Not afterthoughts.' }} />
      {/* ── claude-liam — pdf skill teardown figures ── */}
      <Composition id="PdfAnatomy" component={PdfAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={pdfAnatomySchema}
        defaultProps={{ sparkLine: 'Route to the right library. Never guess.' }} />
      <Composition id="PdfOperations" component={PdfOperations}
        durationInFrames={1020} fps={30} width={1920} height={1080}
        schema={pdfOperationsSchema}
        defaultProps={{ sparkLine: 'Two steps for OCR. Never Unicode subscripts in reportlab.' }} />
      <Composition id="PdfTell" component={PdfTell}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={pdfTellSchema}
        defaultProps={{ sparkLine: 'Three libraries. One routing rule. Two specialist files.' }} />
      {/* ── claude-liam — mcp-builder skill teardown figures ── */}
      <Composition id="McpBuilderAnatomy" component={McpBuilderAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={mcpBuilderAnatomySchema}
        defaultProps={{ sparkLine: 'Research first. Code second. Evaluate third.' }} />
      <Composition id="McpBuilderToolAnatomy" component={McpBuilderToolAnatomy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={mcpBuilderToolAnatomySchema}
        defaultProps={{ sparkLine: 'Name it clearly. Type it strictly. Describe it once.' }} />
      <Composition id="McpBuilderTell" component={McpBuilderTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={mcpBuilderTellSchema}
        defaultProps={{ sparkLine: 'Tool quality = real task completion. Not endpoint count.' }} />
      {/* ── claude-liam — internal-comms skill teardown figures ── */}
      <Composition id="InternalCommsAnatomy" component={InternalCommsAnatomy}
        durationInFrames={780} fps={30} width={1920} height={1080}
        schema={internalCommsAnatomySchema}
        defaultProps={{ sparkLine: 'Identify the type. Load the guide. Follow it exactly.' }} />
      <Composition id="InternalComms3P" component={InternalComms3P}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={internalComms3PSchema}
        defaultProps={{ sparkLine: '30 to 60 seconds. No more.' }} />
      <Composition id="InternalCommsTell" component={InternalCommsTell}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={internalCommsTellSchema}
        defaultProps={{ sparkLine: 'Router, not writer. The guide is the source of truth.' }} />
      {/* ── claude-liam — frontend-design skill teardown figures ── */}
      <Composition id="FrontendDesignAnatomy" component={FrontendDesignAnatomy}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={frontendDesignAnatomySchema}
        defaultProps={{ sparkLine: 'Design for this brief. Not for a similar brief.' }} />
      <Composition id="FrontendDesignProcess" component={FrontendDesignProcess}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={frontendDesignProcessSchema}
        defaultProps={{ sparkLine: 'Plan first. Critique second. Code third.' }} />
      <Composition id="FrontendDesignRestraint" component={FrontendDesignRestraint}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={frontendDesignRestraintSchema}
        defaultProps={{ sparkLine: 'One memorable thing. Everything else quiet.' }} />
      <Composition id="FrontendDesignTell" component={FrontendDesignTell}
        durationInFrames={1020} fps={30} width={1920} height={1080}
        schema={frontendDesignTellSchema}
        defaultProps={{ sparkLine: 'A plan. A critique. Then code.' }} />
      {/* ── claude-liam — docx skill teardown figures ── */}
      <Composition id="DocxAnatomy" component={DocxAnatomy}
        durationInFrames={780} fps={30} width={1920} height={1080}
        schema={docxAnatomySchema}
        defaultProps={{ sparkLine: 'A .docx is just a ZIP of XML.' }} />
      <Composition id="DocxCreate" component={DocxCreate}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={docxCreateSchema}
        defaultProps={{ sparkLine: 'docx-js defaults to A4. Set US Letter explicitly.' }} />
      <Composition id="DocxEdit" component={DocxEdit}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={docxEditSchema}
        defaultProps={{ sparkLine: 'Unpack. Edit XML. Repack. In that order.' }} />
      <Composition id="DocxTell" component={DocxTell}
        durationInFrames={1080} fps={30} width={1920} height={1080}
        schema={docxTellSchema}
        defaultProps={{ sparkLine: 'It is XML. Treat it like XML.' }} />
      {/* ── claude-liam — doc-coauthoring skill teardown figures ── */}
      <Composition id="DocCoauthoringAnatomy" component={DocCoauthoringAnatomy}
        durationInFrames={780} fps={30} width={1920} height={1080}
        schema={docCoauthoringAnatomySchema}
        defaultProps={{ sparkLine: 'Context first. Readers second.' }} />
      <Composition id="DocCoauthoringStage1" component={DocCoauthoringStage1}
        durationInFrames={840} fps={30} width={1920} height={1080}
        schema={docCoauthoringStage1Schema}
        defaultProps={{ sparkLine: 'Dump context. Claude closes the gap.' }} />
      <Composition id="DocCoauthoringStage2" component={DocCoauthoringStage2}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={docCoauthoringStage2Schema}
        defaultProps={{ sparkLine: 'Brainstorm 20. Curate to what matters.' }} />
      <Composition id="DocCoauthoringStage3" component={DocCoauthoringStage3}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={docCoauthoringStage3Schema}
        defaultProps={{ sparkLine: 'A fresh Claude finds your blind spots.' }} />
      <Composition id="DocCoauthoringTell" component={DocCoauthoringTell}
        durationInFrames={1080} fps={30} width={1920} height={1080}
        schema={docCoauthoringTellSchema}
        defaultProps={{ sparkLine: 'Write for the reader. Test with the reader.' }} />
      {/* ── claude-liam — claude-api skill teardown figures ── */}
      <Composition id="ClaudeApiAnatomy" component={ClaudeApiAnatomy}
        durationInFrames={780} fps={30} width={1920} height={1080}
        schema={claudeApiAnatomySchema}
        defaultProps={{ sparkLine: 'Read before you open the file.' }} />
      <Composition id="ClaudeApiSurfaces" component={ClaudeApiSurfaces}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={claudeApiSurfacesSchema}
        defaultProps={{ sparkLine: 'Default to the simplest tier.' }} />
      <Composition id="ClaudeApiDrift" component={ClaudeApiDrift}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={claudeApiDriftSchema}
        defaultProps={{ sparkLine: 'Training data lags the API.' }} />
      <Composition id="ClaudeApiModels" component={ClaudeApiModels}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={claudeApiModelsSchema}
        defaultProps={{ sparkLine: 'Use the exact ID. No date suffixes.' }} />
      <Composition id="ClaudeApiTell" component={ClaudeApiTell}
        durationInFrames={1080} fps={30} width={1920} height={1080}
        schema={claudeApiTellSchema}
        defaultProps={{ sparkLine: '44 pitfalls. All preventable.' }} />
      {/* ── claude-liam — canvas-design skill teardown figures ── */}
      <Composition id="CanvasDesignAnatomy" component={CanvasDesignAnatomy}
        durationInFrames={750} fps={30} width={1920} height={1080}
        schema={canvasDesignAnatomySchema}
        defaultProps={{ sparkLine: 'The philosophy is the brief.' }} />
      <Composition id="CanvasDesignPipeline" component={CanvasDesignPipeline}
        durationInFrames={780} fps={30} width={1920} height={1080}
        schema={canvasDesignPipelineSchema}
        defaultProps={{ sparkLine: 'Claude writes the brief.' }} />
      <Composition id="CanvasDesignPhilosophy" component={CanvasDesignPhilosophy}
        durationInFrames={960} fps={30} width={1920} height={1080}
        schema={canvasDesignPhilosophySchema}
        defaultProps={{ sparkLine: 'Claude writes the brief first.' }} />
      <Composition id="CanvasDesignCanvas" component={CanvasDesignCanvas}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={canvasDesignCanvasSchema}
        defaultProps={{ sparkLine: '90% visual. 10% text.' }} />
      <Composition id="CanvasDesignTell" component={CanvasDesignTell}
        durationInFrames={1080} fps={30} width={1920} height={1080}
        schema={canvasDesignTellSchema}
        defaultProps={{ sparkLine: 'Claude writes the critique too.' }} />
      {/* ── claude-liam — brand-guidelines skill teardown figures ── */}
      <Composition id="BrandGuidelinesAnatomy" component={BrandGuidelinesAnatomy}
        durationInFrames={720} fps={30} width={1920} height={1080}
        schema={brandGuidelinesAnatomySchema}
        defaultProps={{ sparkLine: 'The guide is the code.' }} />
      <Composition id="BrandGuidelinesPipeline" component={BrandGuidelinesPipeline}
        durationInFrames={780} fps={30} width={1920} height={1080}
        schema={brandGuidelinesPipelineSchema}
        defaultProps={{ sparkLine: 'Read, then write.' }} />
      <Composition id="BrandGuidelinesPalette" component={BrandGuidelinesPalette}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={brandGuidelinesPaletteSchema}
        defaultProps={{ sparkLine: 'The exact RGB.' }} />
      <Composition id="BrandGuidelinesTypography" component={BrandGuidelinesTypography}
        durationInFrames={780} fps={30} width={1920} height={1080}
        schema={brandGuidelinesTypographySchema}
        defaultProps={{ sparkLine: '24pt is the line.' }} />
      <Composition id="BrandGuidelinesDesignTell" component={BrandGuidelinesDesignTell}
        durationInFrames={1020} fps={30} width={1920} height={1080}
        schema={brandGuidelinesDesignTellSchema}
        defaultProps={{ sparkLine: 'Constraints, not creativity.' }} />
      {/* ── claude-liam — theme-factory figures ── */}
      <Composition id="ThemeFactoryAnatomy" component={ThemeFactoryAnatomy}
        durationInFrames={721} fps={30} width={1920} height={1080}
        schema={themeFactoryAnatomySchema}
        defaultProps={{ sparkLine: 'A factory in 8 KB.' }} />
      <Composition id="ThemeFactoryThemeCard" component={ThemeFactoryThemeCard}
        durationInFrames={1018} fps={30} width={1920} height={1080}
        schema={themeFactoryThemeCardSchema}
        defaultProps={{ sparkLine: 'A brief, not code.', theme: 'golden-hour' }} />
      <Composition id="ThemeFactoryConsentGate" component={ThemeFactoryConsentGate}
        durationInFrames={818} fps={30} width={1920} height={1080}
        schema={themeFactoryConsentGateSchema}
        defaultProps={{ sparkLine: 'Taste stays human.' }} />
      <Composition id="ThemeFactoryTenSkins" component={ThemeFactoryTenSkins}
        durationInFrames={986} fps={30} width={1920} height={1080}
        schema={themeFactoryTenSkinsSchema}
        defaultProps={{ sparkLine: 'Same plate, ten prints.' }} />
      <Composition id="ThemeFactoryMirror" component={ThemeFactoryMirror}
        durationInFrames={446} fps={30} width={1920} height={1080}
        schema={themeFactoryMirrorSchema}
        defaultProps={{ sparkLine: "You're watching one." }} />
      <Composition id="ThemeFactoryCustomTheme" component={ThemeFactoryCustomTheme}
        durationInFrames={635} fps={30} width={1920} height={1080}
        schema={themeFactoryCustomThemeSchema}
        defaultProps={{ sparkLine: 'The gate survives.' }} />
      <Composition id="ThemeFactoryContrastMeter" component={ThemeFactoryContrastMeter}
        durationInFrames={1232} fps={30} width={1920} height={1080}
        schema={themeFactoryContrastMeterSchema}
        defaultProps={{ sparkLine: 'One load-bearing sentence.' }} />
      {/* ── claude-liam — k12-teacher-skills figures ── */}
      <Composition id="K12Fig01Division" component={K12Fig01Division}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={k12Fig01DivisionSchema}
        defaultProps={{ sparkLine: 'Same hard case. Different door in.' }} />
      <Composition id="K12Fig02CRA" component={K12Fig02CRA}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={k12Fig02CRASchema}
        defaultProps={{ sparkLine: 'Same problem. Different rung to start.' }} />
      <Composition id="K12Fig03TextScaffold" component={K12Fig03TextScaffold}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={k12Fig03TextScaffoldSchema}
        defaultProps={{ sparkLine: 'Same text. Different support structure.' }} />
      <Composition id="K12Fig04WorkingMemory" component={K12Fig04WorkingMemory}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={k12Fig04WorkingMemorySchema}
        defaultProps={{ sparkLine: 'Wrong scaffold. Right problem. Wrong level.' }} />
      <Composition id="K12Fig05DiffVsTrack" component={K12Fig05DiffVsTrack}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={k12Fig05DiffVsTrackSchema}
        defaultProps={{ sparkLine: 'Differentiation widens the path. Tracking forks it.' }} />
      <Composition id="K12Fig06LoadPartition" component={K12Fig06LoadPartition}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={k12Fig06LoadPartitionSchema}
        defaultProps={{ sparkLine: 'The scaffold absorbs extraneous. The learner keeps the germane.' }} />
      <Composition id="K12Fig07ExpertiseReversal" component={K12Fig07ExpertiseReversal}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={k12Fig07ExpertiseReversalSchema}
        defaultProps={{ sparkLine: 'The CRA rung that helped yesterday is noise today.' }} />
      <Composition id="K12Fig08ScaffoldContract" component={K12Fig08ScaffoldContract}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={k12Fig08ScaffoldContractSchema}
        defaultProps={{ sparkLine: 'Scaffolding without fading is dependence with good design.' }} />
      <Composition id="K12Fig09ScaffoldVsCrutch" component={K12Fig09ScaffoldVsCrutch}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={k12Fig09ScaffoldVsCrutchSchema}
        defaultProps={{ sparkLine: "Remove it. Does the learning hold? That's the whole test." }} />
      <Composition id="K12Fig10FadingSchedule" component={K12Fig10FadingSchedule}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={k12Fig10FadingScheduleSchema}
        defaultProps={{ sparkLine: 'One scaffold at a time, until the text stands alone.' }} />
      <Composition id="K12Fig11SubLedger" component={K12Fig11SubLedger}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={k12Fig11SubLedgerSchema}
        defaultProps={{ sparkLine: 'Five roles. Three verdicts. The reader is never substitutable.' }} />
      <Composition id="K12Fig12ColdReadTest" component={K12Fig12ColdReadTest}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={k12Fig12ColdReadTestSchema}
        defaultProps={{ sparkLine: "Cold reads, not rehearsed passages — that's where automaticity lives." }} />
      {/* ── cwc-workshops — Code with Claude 2026 figures ── */}
      <Composition id="CwcMemoryTimeline" component={CwcMemoryTimeline}
        durationInFrames={1080} fps={30} width={1920} height={1080}
        schema={cwcMemoryTimelineSchema}
        defaultProps={{ sparkLine: 'Write once. Recall forever.' }} />
      <Composition id="CwcSixVariants" component={CwcSixVariants}
        durationInFrames={1020} fps={30} width={1920} height={1080}
        schema={cwcSixVariantsSchema}
        defaultProps={{ sparkLine: 'Each change. Measured.' }} />
      <Composition id="CwcFanOutFlow" component={CwcFanOutFlow}
        durationInFrames={1200} fps={30} width={1920} height={1080}
        schema={cwcFanOutFlowSchema}
        defaultProps={{ sparkLine: 'Fan out. Fan in.' }} />
      <Composition id="CwcDecompositionTree" component={CwcDecompositionTree}
        durationInFrames={1260} fps={30} width={1920} height={1080}
        schema={cwcDecompositionTreeSchema}
        defaultProps={{ sparkLine: '402 lines → 15 core + skills.' }} />
      <Composition id="CwcParetoScatter" component={CwcParetoScatter}
        durationInFrames={1140} fps={30} width={1920} height={1080}
        schema={cwcParetoScatterSchema}
        defaultProps={{ sparkLine: 'Sonnet: $0.04, 90%. On the frontier.' }} />
      <Composition id="CwcExclusions" component={CwcExclusions}
        durationInFrames={420} fps={30} width={1920} height={1080}
        schema={cwcExclusionsSchema}
        defaultProps={{ title: 'What this doesn\'t cover', items: ['Example exclusion'], sparkLine: 'Scope is honest.' }} />
      <Composition id="CwcConceptCard" component={CwcConceptCard}
        durationInFrames={360} fps={30} width={1920} height={1080}
        schema={cwcConceptCardSchema}
        defaultProps={{ eyebrow: '', title: 'Concept', body: '', sparkLine: '' }} />
      <Composition id="CwcMemoryQuestion" component={CwcMemoryQuestion}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={cwcMemoryQuestionSchema}
        defaultProps={{ eyebrow: 'AGENT MEMORY', title: 'Why amnesia?', body: 'Sessions are isolated by design.', sparkLine: 'Same agent. Two sessions. No memory.' }} />
      <Composition id="CwcSessionIsolation" component={CwcSessionIsolation}
        durationInFrames={420} fps={30} width={1920} height={1080}
        schema={cwcSessionIsolationSchema}
        defaultProps={{ eyebrow: 'SESSIONS', title: 'Isolated by design', body: 'Each session starts with a blank context window.', sparkLine: 'Each session: clean slate.' }} />
      <Composition id="CwcMemoryProgression" component={CwcMemoryProgression}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={cwcMemoryProgressionSchema}
        defaultProps={{ eyebrow: 'MEMORY', title: 'Three levels', body: 'Isolation → persistence → self-improvement.', sparkLine: 'Isolation → persistence → improvement.' }} />
      <Composition id="CwcEvalQuestion" component={CwcEvalQuestion}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={cwcEvalQuestionSchema}
        defaultProps={{ eyebrow: 'EVALS', title: 'Did it improve?', body: 'Not vibed — measured.', sparkLine: 'Measured, not vibed.' }} />
      <Composition id="CwcTwoLayerEval" component={CwcTwoLayerEval}
        durationInFrames={720} fps={30} width={1920} height={1080}
        schema={cwcTwoLayerEvalSchema}
        defaultProps={{ eyebrow: 'EVAL LAYERS', title: 'Structural + semantic', body: 'Parse metrics programmatically. Grade with an LLM judge.', sparkLine: 'Structural + semantic = signal.' }} />
      <Composition id="CwcVariantAccumulation" component={CwcVariantAccumulation}
        durationInFrames={480} fps={30} width={1920} height={1080}
        schema={cwcVariantAccumulationSchema}
        defaultProps={{ eyebrow: 'ACCUMULATION', title: 'One change per variant', body: 'Each change isolates the delta.', sparkLine: 'Isolate. Measure. Decide.' }} />
      <Composition id="CwcOrchestrationQuestion" component={CwcOrchestrationQuestion}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={cwcOrchestrationQuestionSchema}
        defaultProps={{ eyebrow: 'ORCHESTRATION', title: 'One agent. Many analysts.', body: 'Fan out without blocking.', sparkLine: 'One head. Many analysts. No blocking.' }} />
      <Composition id="CwcFanOutConcept" component={CwcFanOutConcept}
        durationInFrames={840} fps={30} width={1920} height={1080}
        schema={cwcFanOutConceptSchema}
        defaultProps={{ eyebrow: 'FAN-OUT', title: 'Tool call → sessions → results', body: 'The server intercepts, spawns, monitors, and resumes.', sparkLine: 'Tool call → server → sessions → results.' }} />
      <Composition id="CwcSpreadMechanism" component={CwcSpreadMechanism}
        durationInFrames={480} fps={30} width={1920} height={1080}
        schema={cwcSpreadMechanismSchema}
        defaultProps={{ eyebrow: 'SPREAD', title: 'Server coordinates', body: 'The server is the coordinator, not the agent.', sparkLine: 'Server coordinates. Agent decides.' }} />
      <Composition id="CwcDecompositionQuestion" component={CwcDecompositionQuestion}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={cwcDecompositionQuestionSchema}
        defaultProps={{ eyebrow: 'DECOMPOSITION', title: 'Less context. Better decisions.', body: 'Why does cutting the prompt improve reasoning?', sparkLine: 'Less context. Better decisions.' }} />
      <Composition id="CwcThreeLevers" component={CwcThreeLevers}
        durationInFrames={840} fps={30} width={1920} height={1080}
        schema={cwcThreeLeversSchema}
        defaultProps={{ eyebrow: 'THREE LEVERS', title: 'Tools. Skills. Subagents.', body: 'Each trades cost for control differently.', sparkLine: 'Tools. Skills. Subagents.' }} />
      <Composition id="CwcSplitMechanism" component={CwcSplitMechanism}
        durationInFrames={540} fps={30} width={1920} height={1080}
        schema={cwcSplitMechanismSchema}
        defaultProps={{ eyebrow: 'SPLIT', title: 'Load what you need', body: 'Skills load on-demand, not all upfront.', sparkLine: 'Load what you need. When you need it.' }} />
      <Composition id="CwcModelQuestion" component={CwcModelQuestion}
        durationInFrames={300} fps={30} width={1920} height={1080}
        schema={cwcModelQuestionSchema}
        defaultProps={{ eyebrow: 'MODEL SELECTION', title: 'The frontier, not the top', body: 'Which model is actually right for your task?', sparkLine: 'The frontier, not the top.' }} />
      <Composition id="CwcParetoExplained" component={CwcParetoExplained}
        durationInFrames={780} fps={30} width={1920} height={1080}
        schema={cwcParetoExplainedSchema}
        defaultProps={{ eyebrow: 'PARETO', title: 'Non-dominated points', body: 'You cannot improve accuracy without paying more.', sparkLine: 'Non-dominated. On the curve.' }} />
      <Composition id="CwcSweepAccumulation" component={CwcSweepAccumulation}
        durationInFrames={480} fps={30} width={1920} height={1080}
        schema={cwcSweepAccumulationSchema}
        defaultProps={{ eyebrow: 'SWEEP', title: 'Sweep first. Decide after.', body: 'Run all models, plot all results, then choose.', sparkLine: 'Sweep first. Decide after.' }} />
      {/* ── cwc-workshops — expanded deep-dive scenes ── */}
      <Composition id="CwcSkillCallMechanism" component={CwcSkillCallMechanism}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcSkillCallMechanismSchema}
        defaultProps={{ sparkLine: 'Skills keep their complexity to themselves.' }} />
      <Composition id="CwcToolVsSkillComparison" component={CwcToolVsSkillComparison}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcToolVsSkillComparisonSchema}
        defaultProps={{ sparkLine: 'Tools call. Skills think.' }} />
      <Composition id="CwcCostLatencyGain" component={CwcCostLatencyGain}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcCostLatencyGainSchema}
        defaultProps={{ sparkLine: 'Decompose once. Pay less every call.' }} />
      <Composition id="CwcMemorySchema" component={CwcMemorySchema}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcMemorySchemaSchema}
        defaultProps={{ sparkLine: 'The store is just structured facts about users.' }} />
      <Composition id="CwcDreamingService" component={CwcDreamingService}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcDreamingServiceSchema}
        defaultProps={{ sparkLine: 'Dreaming runs between sessions, not during.' }} />
      <Composition id="CwcMemoryRetrieval" component={CwcMemoryRetrieval}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcMemoryRetrievalSchema}
        defaultProps={{ sparkLine: 'Retrieval happens before the first token.' }} />
      <Composition id="CwcFanOutSpeedGain" component={CwcFanOutSpeedGain}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcFanOutSpeedGainSchema}
        defaultProps={{ sparkLine: 'Serial is a queue. Parallel is a wave.' }} />
      <Composition id="CwcResultAggregation" component={CwcResultAggregation}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcResultAggregationSchema}
        defaultProps={{ sparkLine: 'Fan out collects everything. Fan in decides.' }} />
      <Composition id="CwcOrchestrationContract" component={CwcOrchestrationContract}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcOrchestrationContractSchema}
        defaultProps={{ sparkLine: 'The contract is what makes parallelism safe.' }} />
      <Composition id="CwcEvalScoring" component={CwcEvalScoring}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcEvalScoringSchema}
        defaultProps={{ sparkLine: 'Structure first. Semantics second.' }} />
      <Composition id="CwcVariantImprovementWaterfall" component={CwcVariantImprovementWaterfall}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcVariantImprovementWaterfallSchema}
        defaultProps={{ sparkLine: 'Every structured change is a measurable gain.' }} />
      <Composition id="CwcWhenToEval" component={CwcWhenToEval}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcWhenToEvalSchema}
        defaultProps={{ sparkLine: 'No eval, no signal.' }} />
      <Composition id="CwcModelCostComparison" component={CwcModelCostComparison}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcModelCostComparisonSchema}
        defaultProps={{ sparkLine: 'Cost is a variable, not a constraint.' }} />
      <Composition id="CwcFrontierSelection" component={CwcFrontierSelection}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcFrontierSelectionSchema}
        defaultProps={{ sparkLine: 'On the frontier — never off it.' }} />
      <Composition id="CwcSweepInPractice" component={CwcSweepInPractice}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={cwcSweepInPracticeSchema}
        defaultProps={{ sparkLine: 'The sweep is three lines of code.' }} />
      {/* ── claude-liam — profile: Kaustubha Venkata Eluri ── */}
      <Composition id="ProfileKaustubhaFig1Gap" component={ProfileKaustubhaFig1Gap}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileKaustubhaFig1GapSchema}
        defaultProps={{ sparkLine: "If you build it, you're responsible." }} />
      <Composition id="ProfileKaustubhaFig2ModelSystem" component={ProfileKaustubhaFig2ModelSystem}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileKaustubhaFig2ModelSystemSchema}
        defaultProps={{ sparkLine: 'Trustworthiness is a system property.' }} />
      <Composition id="ProfileKaustubhaFig3Projects" component={ProfileKaustubhaFig3Projects}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileKaustubhaFig3ProjectsSchema}
        defaultProps={{ sparkLine: 'Different domains. One discipline.' }} />
      <Composition id="ProfileKaustubhaFig4Resilience" component={ProfileKaustubhaFig4Resilience}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileKaustubhaFig4ResilienceSchema}
        defaultProps={{ sparkLine: 'Degrade gracefully, not catastrophically.' }} />
      <Composition id="ProfileKaustubhaFig5CitedUsed" component={ProfileKaustubhaFig5CitedUsed}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileKaustubhaFig5CitedUsedSchema}
        defaultProps={{ sparkLine: 'The engineering that gets you used.' }} />
      <Composition id="ProfileKaustubhaCredit" component={ProfileKaustubhaCredit}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileKaustubhaCreditSchema}
        defaultProps={{ sparkLine: 'Building systems that keep working.' }} />
      {/* ── claude-liam — profile: Aditi Deodhar ── */}
      <Composition id="ProfileAditiFig1Pivot" component={ProfileAditiFig1Pivot}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileAditiFig1PivotSchema}
        defaultProps={{ sparkLine: 'Stop. Discard. Build what matters.' }} />
      <Composition id="ProfileAditiFig2Stack" component={ProfileAditiFig2Stack}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileAditiFig2StackSchema}
        defaultProps={{ sparkLine: 'Constraint as a design problem.' }} />
      <Composition id="ProfileAditiFig3Builds" component={ProfileAditiFig3Builds}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileAditiFig3BuildsSchema}
        defaultProps={{ sparkLine: 'Gap named. Build. Serves who it missed.' }} />
      <Composition id="ProfileAditiFig4Community" component={ProfileAditiFig4Community}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileAditiFig4CommunitySchema}
        defaultProps={{ sparkLine: "Invisible until it's absent." }} />
      <Composition id="ProfileAditiFig5Record" component={ProfileAditiFig5Record}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileAditiFig5RecordSchema}
        defaultProps={{ sparkLine: 'The number understates the achievement.' }} />
      <Composition id="ProfileAditiFig6Quote" component={ProfileAditiFig6Quote}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileAditiFig6QuoteSchema}
        defaultProps={{ sparkLine: 'The pivot has a cost. She keeps paying it.' }} />
      <Composition id="ProfileAditiCredit" component={ProfileAditiCredit}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={profileAditiCreditSchema}
        defaultProps={{ sparkLine: 'Building what matters, not just what works.' }} />
      {/* ── claude-liam-hai — how-to-explainer-videos figures ── */}
      <Composition id="HaiExplainerFig1Pipeline" component={HaiExplainerFig1Pipeline}
        durationInFrames={480} fps={30} width={1920} height={1080}
        schema={haiExplainerFig1PipelineSchema}
        defaultProps={{ sparkLine: 'Five steps. One sitting.', activeIndex: 4 }} />
      <Composition id="HaiExplainerFig2Folder" component={HaiExplainerFig2Folder}
        durationInFrames={600} fps={30} width={1920} height={1080}
        schema={haiExplainerFig2FolderSchema}
        defaultProps={{ sparkLine: 'One folder = the raw material.' }} />
      <Composition id="HaiExplainerFig3Command" component={HaiExplainerFig3Command}
        durationInFrames={840} fps={30} width={1920} height={1080}
        schema={haiExplainerFig3CommandSchema}
        defaultProps={{ sparkLine: 'The whole pipeline. One command.' }} />
      <Composition id="HaiExplainerFig4Prompt" component={HaiExplainerFig4Prompt}
        durationInFrames={1080} fps={30} width={1920} height={1080}
        schema={haiExplainerFig4PromptSchema}
        defaultProps={{ sparkLine: 'The specifics are what make it yours.' }} />
      <Composition id="HaiExplainerFig5Revise" component={HaiExplainerFig5Revise}
        durationInFrames={660} fps={30} width={1920} height={1080}
        schema={haiExplainerFig5ReviseSchema}
        defaultProps={{ sparkLine: 'Plain language in, better video out.' }} />
      <Composition id="HaiExplainerFig6Publish" component={HaiExplainerFig6Publish}
        durationInFrames={480} fps={30} width={1920} height={1080}
        schema={haiExplainerFig6PublishSchema}
        defaultProps={{ sparkLine: 'Your research deserves an audience.' }} />
      {/* ── HAI Brutalist Fellows Series E01–E12 ── */}
      <Folder name="hai-brutalist-series">
      <Composition id="HaiBrutalistE01Pipeline" component={HaiBrutalistE01Pipeline}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={haiBrutalistE01PipelineSchema}
        defaultProps={{ sparkLine: 'One command. One entry point. One sitting.' }} />
      <Composition id="HaiBrutalistE02Reach" component={HaiBrutalistE02Reach}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={haiBrutalistE02ReachSchema}
        defaultProps={{ sparkLine: 'The work is already done. This gives it a face.' }} />
      <Composition id="HaiBrutalistE03Install" component={HaiBrutalistE03Install}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={haiBrutalistE03InstallSchema}
        defaultProps={{ sparkLine: 'Five minutes from zero to ready.' }} />
      <Composition id="HaiBrutalistE04Folder" component={HaiBrutalistE04Folder}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={haiBrutalistE04FolderSchema}
        defaultProps={{ sparkLine: 'One folder = the raw material.' }} />
      <Composition id="HaiBrutalistE05Command" component={HaiBrutalistE05Command}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={haiBrutalistE05CommandSchema}
        defaultProps={{ sparkLine: 'Awake. Unblocked. End to end.' }} />
      <Composition id="HaiBrutalistE07BeatSheet" component={HaiBrutalistE07BeatSheet}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={haiBrutalistE07BeatSheetSchema}
        defaultProps={{ sparkLine: 'Narration is the master clock.' }} />
      <Composition id="HaiBrutalistE08Voices" component={HaiBrutalistE08Voices}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={haiBrutalistE08VoicesSchema}
        defaultProps={{ sparkLine: 'Free by default. Cloned by choice. Gated always.' }} />
      <Composition id="HaiBrutalistE09Rebuild" component={HaiBrutalistE09Rebuild}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={haiBrutalistE09RebuildSchema}
        defaultProps={{ sparkLine: 'Rebuild the idea as motion. Never screenshot.' }} />
      <Composition id="HaiBrutalistE10Revise" component={HaiBrutalistE10Revise}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={haiBrutalistE10ReviseSchema}
        defaultProps={{ sparkLine: 'Plain language in, better video out.' }} />
      <Composition id="HaiBrutalistE11Publish" component={HaiBrutalistE11Publish}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={haiBrutalistE11PublishSchema}
        defaultProps={{ sparkLine: 'One script. Live in Fellows Research.' }} />
      <Composition id="HaiBrutalistE12Profile" component={HaiBrutalistE12Profile}
        durationInFrames={900} fps={30} width={1920} height={1080}
        schema={haiBrutalistE12ProfileSchema}
        defaultProps={{ sparkLine: 'Make invisible work visible.' }} />
      </Folder>
      {/* ── branding-and-ai — Nina Harris course batch (C01–C12) ── */}
      <Folder name="branding-and-ai">
        <Composition id="BrandSignalMatrix" component={BrandSignalMatrix}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={brandSignalMatrixSchema}
          defaultProps={{ phase: 'result' }} />
        <Composition id="BrandArchetypeWheel" component={BrandArchetypeWheel}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={brandArchetypeWheelSchema}
          defaultProps={{ primaryArchetype: 'Innocent', shadowArchetype: 'Orphan', forcingFunctions: ['Copy tone: warmth, not urgency', 'Visual: bright palette, no dark', 'Features: simplicity first'] }} />
        <Composition id="BrandMetricsTimeline" component={BrandMetricsTimeline}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={brandMetricsTimelineSchema}
          defaultProps={{ patienceGapMonths: 6 }} />
        <Composition id="BrandPipelineAudit" component={BrandPipelineAudit}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={brandPipelineAuditSchema}
          defaultProps={{ highlightRow: 1 }} />
        <Composition id="BrandAgentMapper" component={BrandAgentMapper}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={brandAgentMapperSchema}
          defaultProps={{
            agentMeanings: [
              { label: 'A', desc: 'Function with prompt', checked: true },
              { label: 'B', desc: 'ReAct loop + tools', checked: true },
              { label: 'C', desc: 'Autonomous over horizon', checked: false },
              { label: 'D', desc: 'Specialized pipeline role', checked: false },
            ],
            madisonRoles: [
              { role: 'Intelligence', present: false },
              { role: 'Content', present: false },
              { role: 'Research', present: false },
              { role: 'Experience', present: false },
              { role: 'Performance', present: false },
            ],
            failureLocatability: 'LOW' as const,
          }} />
        <Composition id="BrandVerbScorecard" component={BrandVerbScorecard}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={brandVerbScorecardSchema}
          defaultProps={{
            projects: [
              { name: 'ML GitHub Repo', ideate: 1, build: 3, brand: 0, ship: 0 },
              { name: 'AI Dashboard', ideate: 1, build: 3, brand: 1, ship: 0 },
              { name: 'Data Pipeline', ideate: 2, build: 3, brand: 0, ship: 1 },
            ],
            recommendation: 'Ship: build one project that requires talking to real users before writing any code.',
          }} />
        <Composition id="BrandDriftCaseStudy" component={BrandDriftCaseStudy}
          durationInFrames={360} fps={30} width={1920} height={1080}
          schema={brandDriftCaseStudySchema}
          defaultProps={{ activeColumn: 3 }} />
        <Composition id="BrandAttributionCheck" component={BrandAttributionCheck}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={brandAttributionCheckSchema}
          defaultProps={{ phase: 'checklist' }} />
        <Composition id="BrandVoiceAudit" component={BrandVoiceAudit}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={brandVoiceAuditSchema}
          defaultProps={{ archetype: 'Innocent' }} />
        <Composition id="BrandRepricingTable" component={BrandRepricingTable}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={brandRepricingTableSchema}
          defaultProps={{}} />
        <Composition id="BrandBoondoggleScore" component={BrandBoondoggleScore}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={brandBoondoggleScoreSchema}
          defaultProps={{ score: 45 }} />
        <Composition id="BrandSelfPipeline" component={BrandSelfPipeline}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={brandSelfPipelineSchema}
          defaultProps={{}} />
        {/* ── branding-and-ai — SHOW-DON'T-TELL B01 retrofit ── */}
        <Composition id="BrandB01SignalCollapse" component={BrandB01SignalCollapse}
          durationInFrames={573} fps={30} width={1920} height={1080}
          schema={brandB01SignalCollapseSchema}
          defaultProps={{ sparkLine: 'A signal works only as long as its cost structure holds.' }} />
        <Composition id="BrandB01AlignmentDrift" component={BrandB01AlignmentDrift}
          durationInFrames={542} fps={30} width={1920} height={1080}
          schema={brandB01AlignmentDriftSchema}
          defaultProps={{ sparkLine: 'There was just never a constraint.' }} />
        <Composition id="BrandB01DualTrack" component={BrandB01DualTrack}
          durationInFrames={640} fps={30} width={1920} height={1080}
          schema={brandB01DualTrackSchema}
          defaultProps={{ sparkLine: 'Both true. Neither connected.' }} />
        <Composition id="BrandB01ChainFailure" component={BrandB01ChainFailure}
          durationInFrames={678} fps={30} width={1920} height={1080}
          schema={brandB01ChainFailureSchema}
          defaultProps={{ sparkLine: 'The smallest, most dependent party absorbs everything.' }} />
        <Composition id="BrandB01MonolithGap" component={BrandB01MonolithGap}
          durationInFrames={695} fps={30} width={1920} height={1080}
          schema={brandB01MonolithGapSchema}
          defaultProps={{ sparkLine: 'No seam = no accountability.' }} />
        <Composition id="BrandB01VerbGap" component={BrandB01VerbGap}
          durationInFrames={652} fps={30} width={1920} height={1080}
          schema={brandB01VerbGapSchema}
          defaultProps={{ sparkLine: 'Build was the signal. Now it\'s noise.' }} />
        <Composition id="BrandB01DriftTimeline" component={BrandB01DriftTimeline}
          durationInFrames={702} fps={30} width={1920} height={1080}
          schema={brandB01DriftTimelineSchema}
          defaultProps={{ sparkLine: 'By the time the dashboard shows it — the asset is gone.' }} />
        <Composition id="BrandB01AttributionConfusion" component={BrandB01AttributionConfusion}
          durationInFrames={645} fps={30} width={1920} height={1080}
          schema={brandB01AttributionConfusionSchema}
          defaultProps={{ sparkLine: 'The instinct to find one number is what the problem exploits.' }} />
        <Composition id="BrandB01VoiceConflict" component={BrandB01VoiceConflict}
          durationInFrames={641} fps={30} width={1920} height={1080}
          schema={brandB01VoiceConflictSchema}
          defaultProps={{ sparkLine: 'Both decisions felt reasonable. One was wrong.' }} />
        <Composition id="BrandB01RepricingGap" component={BrandB01RepricingGap}
          durationInFrames={771} fps={30} width={1920} height={1080}
          schema={brandB01RepricingGapSchema}
          defaultProps={{ sparkLine: 'AI tooling is the largest single-year credential cost-structure collapse.' }} />
        <Composition id="BrandB01SeamFailure" component={BrandB01SeamFailure}
          durationInFrames={627} fps={30} width={1920} height={1080}
          schema={brandB01SeamFailureSchema}
          defaultProps={{ sparkLine: 'Most AI failures are seam failures.' }} />
        <Composition id="BrandB01PipelineGap" component={BrandB01PipelineGap}
          durationInFrames={590} fps={30} width={1920} height={1080}
          schema={brandB01PipelineGapSchema}
          defaultProps={{ sparkLine: 'The agent drafts. The plus-one decides.' }} />
        {/* ── branding-and-ai — 9:16 portrait 916 twins (same component, portrait canvas) ── */}
        <Composition id="BrandSignalMatrix916" component={BrandSignalMatrix}
          durationInFrames={300} fps={30} width={1080} height={1920}
          schema={brandSignalMatrixSchema}
          defaultProps={{ phase: 'result' }} />
        <Composition id="BrandArchetypeWheel916" component={BrandArchetypeWheel}
          durationInFrames={300} fps={30} width={1080} height={1920}
          schema={brandArchetypeWheelSchema}
          defaultProps={{ primaryArchetype: 'Innocent', shadowArchetype: 'Orphan', forcingFunctions: ['Copy tone: warmth, not urgency', 'Visual: bright palette, no dark', 'Features: simplicity first'] }} />
        <Composition id="BrandMetricsTimeline916" component={BrandMetricsTimeline}
          durationInFrames={300} fps={30} width={1080} height={1920}
          schema={brandMetricsTimelineSchema}
          defaultProps={{ patienceGapMonths: 6 }} />
        <Composition id="BrandPipelineAudit916" component={BrandPipelineAudit}
          durationInFrames={300} fps={30} width={1080} height={1920}
          schema={brandPipelineAuditSchema}
          defaultProps={{ highlightRow: 1 }} />
        <Composition id="BrandAgentMapper916" component={BrandAgentMapper}
          durationInFrames={300} fps={30} width={1080} height={1920}
          schema={brandAgentMapperSchema}
          defaultProps={{
            agentMeanings: [
              { label: 'A', desc: 'Function with prompt', checked: true },
              { label: 'B', desc: 'ReAct loop + tools', checked: true },
              { label: 'C', desc: 'Autonomous over horizon', checked: false },
              { label: 'D', desc: 'Specialized pipeline role', checked: false },
            ],
            madisonRoles: [
              { role: 'Intelligence', present: false },
              { role: 'Content', present: false },
              { role: 'Research', present: false },
              { role: 'Experience', present: false },
              { role: 'Performance', present: false },
            ],
            failureLocatability: 'LOW' as const,
          }} />
        <Composition id="BrandVerbScorecard916" component={BrandVerbScorecard}
          durationInFrames={300} fps={30} width={1080} height={1920}
          schema={brandVerbScorecardSchema}
          defaultProps={{
            projects: [
              { name: 'ML GitHub Repo', ideate: 1, build: 3, brand: 0, ship: 0 },
              { name: 'AI Dashboard', ideate: 1, build: 3, brand: 1, ship: 0 },
              { name: 'Data Pipeline', ideate: 2, build: 3, brand: 0, ship: 1 },
            ],
            recommendation: 'Ship: build one project that requires talking to real users before writing any code.',
          }} />
        <Composition id="BrandDriftCaseStudy916" component={BrandDriftCaseStudy}
          durationInFrames={360} fps={30} width={1080} height={1920}
          schema={brandDriftCaseStudySchema}
          defaultProps={{ activeColumn: 3 }} />
        <Composition id="BrandAttributionCheck916" component={BrandAttributionCheck}
          durationInFrames={300} fps={30} width={1080} height={1920}
          schema={brandAttributionCheckSchema}
          defaultProps={{ phase: 'checklist' }} />
        <Composition id="BrandVoiceAudit916" component={BrandVoiceAudit}
          durationInFrames={300} fps={30} width={1080} height={1920}
          schema={brandVoiceAuditSchema}
          defaultProps={{ archetype: 'Innocent' }} />
        <Composition id="BrandRepricingTable916" component={BrandRepricingTable}
          durationInFrames={300} fps={30} width={1080} height={1920}
          schema={brandRepricingTableSchema}
          defaultProps={{}} />
        <Composition id="BrandBoondoggleScore916" component={BrandBoondoggleScore}
          durationInFrames={300} fps={30} width={1080} height={1920}
          schema={brandBoondoggleScoreSchema}
          defaultProps={{ score: 45 }} />
        <Composition id="BrandSelfPipeline916" component={BrandSelfPipeline}
          durationInFrames={300} fps={30} width={1080} height={1920}
          schema={brandSelfPipelineSchema}
          defaultProps={{}} />
        <Composition id="BrandB01SignalCollapse916" component={BrandB01SignalCollapse}
          durationInFrames={573} fps={30} width={1080} height={1920}
          schema={brandB01SignalCollapseSchema}
          defaultProps={{ sparkLine: 'A signal works only as long as its cost structure holds.' }} />
        <Composition id="BrandB01AlignmentDrift916" component={BrandB01AlignmentDrift}
          durationInFrames={542} fps={30} width={1080} height={1920}
          schema={brandB01AlignmentDriftSchema}
          defaultProps={{ sparkLine: 'There was just never a constraint.' }} />
        <Composition id="BrandB01DualTrack916" component={BrandB01DualTrack}
          durationInFrames={640} fps={30} width={1080} height={1920}
          schema={brandB01DualTrackSchema}
          defaultProps={{ sparkLine: 'Both true. Neither connected.' }} />
        <Composition id="BrandB01ChainFailure916" component={BrandB01ChainFailure}
          durationInFrames={678} fps={30} width={1080} height={1920}
          schema={brandB01ChainFailureSchema}
          defaultProps={{ sparkLine: 'The smallest, most dependent party absorbs everything.' }} />
        <Composition id="BrandB01MonolithGap916" component={BrandB01MonolithGap}
          durationInFrames={695} fps={30} width={1080} height={1920}
          schema={brandB01MonolithGapSchema}
          defaultProps={{ sparkLine: 'No seam = no accountability.' }} />
        <Composition id="BrandB01VerbGap916" component={BrandB01VerbGap}
          durationInFrames={652} fps={30} width={1080} height={1920}
          schema={brandB01VerbGapSchema}
          defaultProps={{ sparkLine: "Build was the signal. Now it's noise." }} />
        <Composition id="BrandB01DriftTimeline916" component={BrandB01DriftTimeline}
          durationInFrames={702} fps={30} width={1080} height={1920}
          schema={brandB01DriftTimelineSchema}
          defaultProps={{ sparkLine: 'By the time the dashboard shows it — the asset is gone.' }} />
        <Composition id="BrandB01AttributionConfusion916" component={BrandB01AttributionConfusion}
          durationInFrames={645} fps={30} width={1080} height={1920}
          schema={brandB01AttributionConfusionSchema}
          defaultProps={{ sparkLine: 'The instinct to find one number is what the problem exploits.' }} />
        <Composition id="BrandB01VoiceConflict916" component={BrandB01VoiceConflict}
          durationInFrames={641} fps={30} width={1080} height={1920}
          schema={brandB01VoiceConflictSchema}
          defaultProps={{ sparkLine: 'Both decisions felt reasonable. One was wrong.' }} />
        <Composition id="BrandB01RepricingGap916" component={BrandB01RepricingGap}
          durationInFrames={771} fps={30} width={1080} height={1920}
          schema={brandB01RepricingGapSchema}
          defaultProps={{ sparkLine: 'AI tooling is the largest single-year credential cost-structure collapse.' }} />
        <Composition id="BrandB01SeamFailure916" component={BrandB01SeamFailure}
          durationInFrames={627} fps={30} width={1080} height={1920}
          schema={brandB01SeamFailureSchema}
          defaultProps={{ sparkLine: 'Most AI failures are seam failures.' }} />
        <Composition id="BrandB01PipelineGap916" component={BrandB01PipelineGap}
          durationInFrames={590} fps={30} width={1080} height={1920}
          schema={brandB01PipelineGapSchema}
          defaultProps={{ sparkLine: 'The agent drafts. The plus-one decides.' }} />
      </Folder>
      {/* ── claude-liam — vercel-mcp figures ── */}
      <Folder name="Vercel-Trusted">
        <Composition id="VercelOfficial" component={VercelOfficial}
          durationInFrames={834} fps={30} width={1920} height={1080}
          schema={vercelOfficialSchema}
          defaultProps={vercelOfficialSchema.parse({})} />
        <Composition id="VercelDiagnose" component={VercelDiagnose}
          durationInFrames={776} fps={30} width={1920} height={1080}
          schema={vercelDiagnoseSchema}
          defaultProps={vercelDiagnoseSchema.parse({})} />
        <Composition id="VercelAccountEquivalent" component={VercelAccountEquivalent}
          durationInFrames={832} fps={30} width={1920} height={1080}
          schema={vercelAccountEquivalentSchema}
          defaultProps={vercelAccountEquivalentSchema.parse({})} />
        <Composition id="VercelBuyDomain" component={VercelBuyDomain}
          durationInFrames={1064} fps={30} width={1920} height={1080}
          schema={vercelBuyDomainSchema}
          defaultProps={vercelBuyDomainSchema.parse({})} />
        <Composition id="VercelSafeguardGap" component={VercelSafeguardGap}
          durationInFrames={942} fps={30} width={1920} height={1080}
          schema={vercelSafeguardGapSchema}
          defaultProps={vercelSafeguardGapSchema.parse({})} />
        <Composition id="VercelOwnGuidance" component={VercelOwnGuidance}
          durationInFrames={1041} fps={30} width={1920} height={1080}
          schema={vercelOwnGuidanceSchema}
          defaultProps={vercelOwnGuidanceSchema.parse({})} />
        <Composition id="VercelMitigations" component={VercelMitigations}
          durationInFrames={1121} fps={30} width={1920} height={1080}
          schema={vercelMitigationsSchema}
          defaultProps={vercelMitigationsSchema.parse({})} />
      </Folder>
      {/* ── claude-liam-a5a — "Wrap It & Test It" series figures ── */}
      <Folder name="A5a-WrapIt">
        <Composition id="A5aFrameworkChoice" component={A5aFrameworkChoice}
          durationInFrames={799} fps={30} width={1920} height={1080}
          schema={a5aFrameworkChoiceSchema}
          defaultProps={a5aFrameworkChoiceSchema.parse({})} />
        <Composition id="A5aInputWiring" component={A5aInputWiring}
          durationInFrames={1038} fps={30} width={1920} height={1080}
          schema={a5aInputWiringSchema}
          defaultProps={a5aInputWiringSchema.parse({})} />
        <Composition id="A5aOutputFormat" component={A5aOutputFormat}
          durationInFrames={898} fps={30} width={1920} height={1080}
          schema={a5aOutputFormatSchema}
          defaultProps={a5aOutputFormatSchema.parse({})} />
      </Folder>
      {/* ── claude-liam-a8 — "Ship It" series figures ── */}
      <Folder name="A8-ShipIt">
        <Composition id="A8DeliverableMap" component={A8DeliverableMap}
          durationInFrames={663} fps={30} width={1920} height={1080}
          schema={a8DeliverableMapSchema}
          defaultProps={a8DeliverableMapSchema.parse({})} />
        <Composition id="A8ShipItRule" component={A8ShipItRule}
          durationInFrames={423} fps={30} width={1920} height={1080}
          schema={a8ShipItRuleSchema}
          defaultProps={a8ShipItRuleSchema.parse({})} />
      </Folder>
      {/* ── claude-liam — connect-linkedin figures ── */}
      <Folder name="LinkedIn-Gated">
        <Composition id="LinkedInTrustBoundary" component={LinkedInTrustBoundary}
          durationInFrames={864} fps={30} width={1920} height={1080}
          schema={linkedInTrustBoundarySchema}
          defaultProps={linkedInTrustBoundarySchema.parse({})} />
        <Composition id="LinkedInThreeLanes" component={LinkedInThreeLanes}
          durationInFrames={774} fps={30} width={1920} height={1080}
          schema={linkedInThreeLanesSchema}
          defaultProps={linkedInThreeLanesSchema.parse({})} />
        <Composition id="LinkedInAsymmetry" component={LinkedInAsymmetry}
          durationInFrames={831} fps={30} width={1920} height={1080}
          schema={linkedInAsymmetrySchema}
          defaultProps={linkedInAsymmetrySchema.parse({})} />
        <Composition id="LinkedInApiSurface" component={LinkedInApiSurface}
          durationInFrames={1044} fps={30} width={1920} height={1080}
          schema={linkedInApiSurfaceSchema}
          defaultProps={linkedInApiSurfaceSchema.parse({})} />
        <Composition id="LinkedInDetectionStack" component={LinkedInDetectionStack}
          durationInFrames={1209} fps={30} width={1920} height={1080}
          schema={linkedInDetectionStackSchema}
          defaultProps={linkedInDetectionStackSchema.parse({})} />
        <Composition id="LinkedInLegalSplit" component={LinkedInLegalSplit}
          durationInFrames={1184} fps={30} width={1920} height={1080}
          schema={linkedInLegalSplitSchema}
          defaultProps={linkedInLegalSplitSchema.parse({})} />
        <Composition id="LinkedInRedFlags" component={LinkedInRedFlags}
          durationInFrames={1081} fps={30} width={1920} height={1080}
          schema={linkedInRedFlagsSchema}
          defaultProps={linkedInRedFlagsSchema.parse({})} />
      </Folder>
      {/* ── generic skill-teardown templates (meta-series batch) ── */}
      <Folder name="SkillTeardown-Generic">
        <Composition id="SkillTeardownAnatomy" component={SkillTeardownAnatomy}
          durationInFrames={600} fps={30} width={1920} height={1080}
          schema={skillTeardownAnatomySchema}
          defaultProps={skillTeardownAnatomySchema.parse({})} />
        <Composition id="SkillTeardownPipeline" component={SkillTeardownPipeline}
          durationInFrames={600} fps={30} width={1920} height={1080}
          schema={skillTeardownPipelineSchema}
          defaultProps={skillTeardownPipelineSchema.parse({})} />
        <Composition id="SkillTeardownMechanism" component={SkillTeardownMechanism}
          durationInFrames={600} fps={30} width={1920} height={1080}
          schema={skillTeardownMechanismSchema}
          defaultProps={skillTeardownMechanismSchema.parse({})} />
      </Folder>
      {/* ── claude-liam-fluency-trap — reel-local compositions ── */}
      {/* ── claude-liam-what-a-university-can-require — reel-local compositions ── */}
      {/* ── claude-liam-riff-the-outros — reel-local compositions ── */}
      <Folder name="OutroRiff">
        <Composition id="RiffSplit" component={RiffSplit}
          durationInFrames={420} fps={30} width={1920} height={1080}
          schema={riffSplitSchema}
          defaultProps={riffSplitSchema.parse({
            left:  { label: 'Mascot card', sub: 'drawn in code', assets: 'none', channels: '@NikBearBrown' },
            right: { label: 'Logo sting',  sub: 'mark + jingle',  assets: 'svg + mp3', channels: 'everyone else' },
          })} />
        <Composition id="RiffLottery" component={RiffLottery}
          durationInFrames={420} fps={30} width={1920} height={1080}
          schema={riffLotterySchema}
          defaultProps={riffLotterySchema.parse({ chips: ['spring', 'drawOn', 'rotation', 'kineticGrid'] })} />
      </Folder>
      <Folder name="RequireReport">
        <Composition id="ReqSegmentCard" component={ReqSegmentCard}
          durationInFrames={240} fps={30} width={1920} height={1080}
          schema={reqSegmentCardSchema}
          defaultProps={reqSegmentCardSchema.parse({})} />
        <Composition id="ReqBars" component={ReqBars}
          durationInFrames={420} fps={30} width={1920} height={1080}
          schema={reqBarsSchema}
          defaultProps={reqBarsSchema.parse({ data: [{ label: 'Reducing long-term learning', value: 88 }, { label: 'Cognitive capacity', value: 87 }] })} />
        <Composition id="ReqLedger" component={ReqLedger}
          durationInFrames={480} fps={30} width={1920} height={1080}
          schema={reqLedgerSchema}
          defaultProps={reqLedgerSchema.parse({ rows: [{ label: 'Publish baseline rules' }, { label: 'Update the academic codes' }] })} />
        <Composition id="ReqDefinitionDrop" component={ReqDefinitionDrop}
          durationInFrames={420} fps={30} width={1920} height={1080}
          schema={reqDefinitionDropSchema}
          defaultProps={reqDefinitionDropSchema.parse({ parts: ['the technology', 'its strengths and weaknesses'] })} />
        <Composition id="ReqLevers" component={ReqLevers}
          durationInFrames={420} fps={30} width={1920} height={1080}
          schema={reqLeversSchema}
          defaultProps={reqLeversSchema.parse({ levers: [{ name: 'The syllabus' }] })} />
        <Composition id="ReqRingWord" component={ReqRingWord}
          durationInFrames={390} fps={30} width={1920} height={1080}
          schema={reqRingWordSchema}
          defaultProps={reqRingWordSchema.parse({})} />
      </Folder>
      <Folder name="TrainTeacher">
        <Composition id="TtTwoAnswers" component={TtTwoAnswers}
          durationInFrames={420} fps={30} width={1920} height={1080}
          schema={ttTwoAnswersSchema}
          defaultProps={ttTwoAnswersSchema.parse({ left: { name: 'Ban the phone' }, right: { name: 'Buy the platform' } })} />
        <Composition id="TtFrontLoaded" component={TtFrontLoaded}
          durationInFrames={450} fps={30} width={1920} height={1080}
          schema={ttFrontLoadedSchema}
          defaultProps={ttFrontLoadedSchema.parse({})} />
        <Composition id="TtCorrection" component={TtCorrection}
          durationInFrames={450} fps={30} width={1920} height={1080}
          schema={ttCorrectionSchema}
          defaultProps={ttCorrectionSchema.parse({ before: 'Suspensions increased 30 percent for ', wrong: 'Black boys', after: '.', corrected: 'In-school suspensions rose about 30% for Black students. No significant effect on out-of-school suspensions.' })} />
        <Composition id="TtNullResult" component={TtNullResult}
          durationInFrames={450} fps={30} width={1920} height={1080}
          schema={ttNullResultSchema}
          defaultProps={ttNullResultSchema.parse({ left: { label: 'Teacher knowledge', value: 62 }, right: { label: 'Student achievement', value: 0 } })} />
        <Composition id="TtScaleDecay" component={TtScaleDecay}
          durationInFrames={450} fps={30} width={1920} height={1080}
          schema={ttScaleDecaySchema}
          defaultProps={ttScaleDecaySchema.parse({ stops: [{ scaleLabel: 'Small efficacy trials', effect: 0.31 }, { scaleLabel: 'Large effectiveness trials', effect: 0.11 }] })} />
        <Composition id="TtDenominator" component={TtDenominator}
          durationInFrames={480} fps={30} width={1920} height={1080}
          schema={ttDenominatorSchema}
          defaultProps={ttDenominatorSchema.parse({})} />
        <Composition id="TtAbsence" component={TtAbsence}
          durationInFrames={480} fps={30} width={1920} height={1080}
          schema={ttAbsenceSchema}
          defaultProps={ttAbsenceSchema.parse({})} />
        <Composition id="TtVerdictGrid" component={TtVerdictGrid}
          durationInFrames={540} fps={30} width={1920} height={1080}
          schema={ttVerdictGridSchema}
          defaultProps={ttVerdictGridSchema.parse({ rows: [{ claim: 'Teacher training moderates EdTech effectiveness', verdict: 'SUPPORTED' }, { claim: 'Sustained AI-specific PD improves student outcomes', verdict: 'NO EVIDENCE' }] })} />
        <Composition id="TtEffectBars" component={TtEffectBars}
          durationInFrames={450} fps={30} width={1920} height={1080}
          schema={ttEffectBarsSchema}
          defaultProps={ttEffectBarsSchema.parse({ data: [{ label: 'Instructional practice', value: 49, display: '0.49 SD' }, { label: 'Student achievement', value: 18, display: '0.18 SD', accent: true }] })} />
      </Folder>
      <Folder name="FluencyTrap">
        <Composition id="FluencySegmentCard" component={FluencySegmentCard}
          durationInFrames={240} fps={30} width={1920} height={1080}
          schema={fluencySegmentCardSchema}
          defaultProps={fluencySegmentCardSchema.parse({})} />
        <Composition id="FluencyDivergence" component={FluencyDivergence}
          durationInFrames={480} fps={30} width={1920} height={1080}
          schema={fluencyDivergenceSchema}
          defaultProps={fluencyDivergenceSchema.parse({})} />
        <Composition id="FluencyThreshold" component={FluencyThreshold}
          durationInFrames={420} fps={30} width={1920} height={1080}
          schema={fluencyThresholdSchema}
          defaultProps={fluencyThresholdSchema.parse({})} />
        <Composition id="FluencySourceFlow" component={FluencySourceFlow}
          durationInFrames={480} fps={30} width={1920} height={1080}
          schema={fluencySourceFlowSchema}
          defaultProps={fluencySourceFlowSchema.parse({})} />
        <Composition id="FluencyScale" component={FluencyScale}
          durationInFrames={420} fps={30} width={1920} height={1080}
          schema={fluencyScaleSchema}
          defaultProps={fluencyScaleSchema.parse({})} />
        <Composition id="FluencyVerdictStamps" component={FluencyVerdictStamps}
          durationInFrames={500} fps={30} width={1920} height={1080}
          schema={fluencyVerdictStampsSchema}
          defaultProps={fluencyVerdictStampsSchema.parse({})} />
        <Composition id="FluencyChipGrid" component={FluencyChipGrid}
          durationInFrames={486} fps={30} width={1920} height={1080}
          schema={fluencyChipGridSchema}
          defaultProps={fluencyChipGridSchema.parse({})} />
      </Folder>
      {/* ── claude-liam-dashboard-that-lied — reel-local compositions ── */}
      <Folder name="DashboardThatLied">
        <Composition id="DtlScale" component={DtlScale}
          durationInFrames={480} fps={30} width={1920} height={1080}
          schema={dtlScaleSchema}
          defaultProps={dtlScaleSchema.parse({})} />
        <Composition id="DtlChipGrid" component={DtlChipGrid}
          durationInFrames={510} fps={30} width={1920} height={1080}
          schema={dtlChipGridSchema}
          defaultProps={dtlChipGridSchema.parse({})} />
        <Composition id="DtlLayerStack" component={DtlLayerStack}
          durationInFrames={540} fps={30} width={1920} height={1080}
          schema={dtlLayerStackSchema}
          defaultProps={dtlLayerStackSchema.parse({})} />
      </Folder>
      {/* ── logo-motion — parametric logo stings (skills/make/logo-motion) ──
          ONE composition for every mark. Length is a prop: calculateMetadata
          turns durationInSeconds into durationInFrames, and every ramp in the
          scene is a fraction of the total, so the animation re-times instead
          of truncating. Add a mark by adding a logos/<name>.ts and a key to
          the LOGOS registry — never by copying this block. */}
      <Folder name="LogoMotion">
        <Composition id="LogoMotion" component={LogoMotion}
          durationInFrames={180} fps={30} width={1920} height={1080}
          schema={logoMotionSchema}
          defaultProps={logoMotionSchema.parse({})}
          calculateMetadata={({props}) => ({
            durationInFrames: Math.max(1, Math.round(props.durationInSeconds * 30)),
          })} />
      </Folder>

      {/* ── finance skill — four chart shapes (SKILL.md §Shape logic, locked) ── */}
      <Folder name="Finance-Charts">
        <Composition id="GodotDesignBoard" component={GodotDesignBoard}
          schema={godotDesignBoardSchema} width={1920} height={1080} fps={30} durationInFrames={600}
          defaultProps={godotDesignBoardSchema.parse({title:'Design to evidence',section:'GDD',excerpt:'Supply an exact document excerpt.',source:'Source required',status:'PROPOSED',visualLabel:'Design explanation',cards:[{label:'Intent',text:'Supply the actual design requirement.'}]})}
          calculateMetadata={({props})=>({durationInFrames:Math.ceil(props.durationSeconds*30)})}/>
        <Composition id="GodotDesignBoard916" component={GodotDesignBoard}
          schema={godotDesignBoardSchema} width={1080} height={1920} fps={30} durationInFrames={600}
          defaultProps={godotDesignBoardSchema.parse({title:'Design to evidence',section:'GDD',excerpt:'Supply an exact document excerpt.',source:'Source required',status:'PROPOSED',visualLabel:'Design explanation',cards:[{label:'Intent',text:'Supply the actual design requirement.'}]})}
          calculateMetadata={({props})=>({durationInFrames:Math.ceil(props.durationSeconds*30)})}/>
        <Composition id="GodotDesignFigure" component={GodotDesignFigure}
          schema={godotDesignFigureSchema} width={1920} height={1080} fps={30} durationInFrames={600}
          defaultProps={godotDesignFigureSchema.parse({title:'Design figure',status:'PROPOSED',image:'',source:'Source required',cards:[{label:'Intent',text:'Supply the design requirement.'}]})}
          calculateMetadata={({props})=>({durationInFrames:Math.ceil(props.durationSeconds*30)})}/>
        <Composition id="GodotDesignFigure916" component={GodotDesignFigure}
          schema={godotDesignFigureSchema} width={1080} height={1920} fps={30} durationInFrames={600}
          defaultProps={godotDesignFigureSchema.parse({title:'Design figure',status:'PROPOSED',image:'',source:'Source required',cards:[{label:'Intent',text:'Supply the design requirement.'}]})}
          calculateMetadata={({props})=>({durationInFrames:Math.ceil(props.durationSeconds*30)})}/>
        <Composition id="GodotDevWorkbench" component={GodotDevWorkbench}
          durationInFrames={450} fps={30} width={1920} height={1080}
          schema={godotDevWorkbenchSchema}
          defaultProps={godotDevWorkbenchSchema.parse({mode:'code',title:'Inspect the Game',project:'Godot project',source:'Supply verified source excerpts'})}
          calculateMetadata={({props})=>({durationInFrames:Math.ceil(props.durationSeconds*30)})}/>
        <Composition id="GodotDevWorkbench916" component={GodotDevWorkbench}
          durationInFrames={450} fps={30} width={1080} height={1920}
          schema={godotDevWorkbenchSchema}
          defaultProps={godotDevWorkbenchSchema.parse({mode:'code',title:'Inspect the Game',project:'Godot project',source:'Supply verified source excerpts'})}
          calculateMetadata={({props})=>({durationInFrames:Math.ceil(props.durationSeconds*30)})}/>
        <Composition id="WalkerGodotSetup" component={WalkerGodotSetup}
          durationInFrames={360} fps={24} width={1920} height={1080}
          schema={walkerGodotSetupSchema}
          defaultProps={walkerGodotSetupSchema.parse({mode:'download',title:'Download Godot',version:'4.7.2'})}
          calculateMetadata={({props})=>({durationInFrames:Math.ceil(props.durationSeconds*24)})}/>
        <Composition id="WalkerGodotSetup916" component={WalkerGodotSetup}
          durationInFrames={360} fps={24} width={1080} height={1920}
          schema={walkerGodotSetupSchema}
          defaultProps={walkerGodotSetupSchema.parse({mode:'download',title:'Download Godot',version:'4.7.2'})}
          calculateMetadata={({props})=>({durationInFrames:Math.ceil(props.durationSeconds*24)})}/>
        {/* claude-liam-hesitant — the Beat 2 hesitant-writer overview (EXECUTIVE-SUMMARY LAW) */}
        <Composition
          id="BrutalistHesitantWriter"
          component={BrutalistHesitantWriter}
          durationInFrames={606}
          calculateMetadata={({props}) => ({durationInFrames: Math.ceil(((props as any).durationSeconds ?? 20.2) * 30)})}
          fps={30}
          width={1920}
          height={1080}
          schema={brutalistHesitantWriterSchema}
          defaultProps={brutalistHesitantWriterDemoDefaultProps}
        />
        <Composition
          id="BrutalistHesitantWriter916"
          component={BrutalistHesitantWriter}
          durationInFrames={606}
          fps={30}
          width={1080}
          height={1920}
          schema={brutalistHesitantWriterSchema}
          defaultProps={brutalistHesitantWriterDemoDefaultProps}
        />
        <Composition
          id="BrutalistHesitantWriterSq"
          component={BrutalistHesitantWriter}
          durationInFrames={606}
          fps={30}
          width={1080}
          height={1080}
          schema={brutalistHesitantWriterSchema}
          defaultProps={brutalistHesitantWriterDemoDefaultProps}
        />
        {/* B04 / B05 — Flow → Sankey. Income statement or cash flow. */}
        <Composition
          id="FinanceSankey"
          component={FinanceSankey}
          durationInFrames={480}
          fps={30}
          width={1920}
          height={1080}
          schema={financeSankeySchema}
          defaultProps={financeSankeySchema.parse({
            title: 'NVDA FY2026 — Income Statement',
            subtitle: 'Revenue to Net Income',
            statement: 'income' as const,
            nodes: [
              { id: 'rev',    label: 'Revenue',          value: 215.9, column: 0, color: 'total'   as const },
              { id: 'cogs',   label: 'Cost of Revenue',  value: 62.5,  column: 1, color: 'outflow' as const },
              { id: 'gp',     label: 'Gross Profit',     value: 153.5, column: 1, color: 'inflow'  as const },
              { id: 'opex',   label: 'Operating Exp.',   value: 23.1,  column: 2, color: 'outflow' as const },
              { id: 'ebit',   label: 'Operating Income', value: 130.4, column: 2, color: 'inflow'  as const },
              { id: 'taxoth', label: 'Tax & Other',      value: 10.3,  column: 3, color: 'outflow' as const },
              { id: 'ni',     label: 'Net Income',       value: 120.1, column: 3, color: 'inflow'  as const },
            ],
            links: [
              { source: 'rev',  target: 'cogs',   value: 62.5,  color: 'outflow' as const, estimate: false },
              { source: 'rev',  target: 'gp',     value: 153.5, color: 'inflow'  as const, estimate: false },
              { source: 'gp',   target: 'opex',   value: 23.1,  color: 'outflow' as const, estimate: false },
              { source: 'gp',   target: 'ebit',   value: 130.4, color: 'inflow'  as const, estimate: false },
              { source: 'ebit', target: 'taxoth', value: 10.3,  color: 'outflow' as const, estimate: false },
              { source: 'ebit', target: 'ni',     value: 120.1, color: 'inflow'  as const, estimate: false },
            ],
            unit:      '$B',
            source:    'NVDA 10-K FY2026, SEC EDGAR XBRL',
            sparkLine: '71.1% gross margin. 55.6% net.',
          })}
        />
        {/* B06 — Snapshot → mirrored bar. Balance sheet. NEVER a Sankey. */}
        <Composition
          id="FinanceMirroredBar"
          component={FinanceMirroredBar}
          durationInFrames={480}
          fps={30}
          width={1920}
          height={1080}
          schema={financeMirroredBarSchema}
          defaultProps={financeMirroredBarSchema.parse({
            title:      'NVDA FY2026 — Balance Sheet',
            subtitle:   'Period ending 2026-01-25',
            leftLabel:  'Assets',
            rightLabel: 'Liabilities & Equity',
            leftItems: [
              { label: 'Current Assets',     pct: 42.1, value: '$87.1B', color: 'inflow'  as const, estimate: false, isSubtotal: false },
              { label: 'Non-Current Assets', pct: 57.9, value: '$119.7B',color: 'other'   as const, estimate: false, isSubtotal: false },
            ],
            rightItems: [
              { label: 'Current Liabilities',   pct: 12.1, value: '$25.0B', color: 'outflow' as const, estimate: false, isSubtotal: false },
              { label: 'Long-term Liabilities', pct: 11.8, value: '$24.5B', color: 'outflow' as const, estimate: false, isSubtotal: false },
              { label: 'Shareholders Equity',   pct: 76.1, value: '$157.3B',color: 'inflow'  as const, estimate: false, isSubtotal: true  },
            ],
            totalValue: '$206.8B',
            source:     'NVDA 10-K FY2026, SEC EDGAR XBRL',
            sparkLine:  'Equity-to-assets 76%. Net cash position.',
          })}
        />
        {/* B07 — Composition × time → stacked bar. Segments. */}
        <Composition
          id="FinanceStackedBar"
          component={FinanceStackedBar}
          durationInFrames={480}
          fps={30}
          width={1920}
          height={1080}
          schema={financeStackedBarSchema}
          defaultProps={financeStackedBarSchema.parse({
            title:    'NVDA — Revenue by Segment',
            subtitle: 'FY2024–FY2026',
            periods:  ['FY2024', 'FY2025', 'FY2026'],
            segments: [
              { label: 'Data Center',              color: 'inflow'  as const, values: [47.5,  115.2, 187.0], estimates: [false, false, false] },
              { label: 'Gaming',                   color: 'outflow' as const, values: [10.4,   11.3,  11.0], estimates: [false, false, false] },
              { label: 'Professional Visualization',color: 'other'  as const, values: [1.6,    1.9,   4.5],  estimates: [false, false, false] },
              { label: 'Automotive',               color: 'total'   as const, values: [1.1,    1.7,   5.0],  estimates: [false, false, false] },
              { label: 'OEM & Other',              color: 'subject' as const, values: [0.4,    0.4,   8.5],  estimates: [false, false, true  ] },
            ],
            unit:      '$B',
            normalize: false,
            source:    'NVDA 10-K FY2026, SEC EDGAR XBRL',
            sparkLine: 'Data Center: 87% of FY2026 revenue.',
          })}
        />
        {/* B08 — Distribution → dot-plot. Sector comparator. Subject lands wherever it lands. */}
        <Composition
          id="FinanceDotPlot"
          component={FinanceDotPlot}
          durationInFrames={480}
          fps={30}
          width={1920}
          height={1080}
          schema={financeDotPlotSchema}
          defaultProps={financeDotPlotSchema.parse({
            title:    'Gross Margin — Semiconductor Sector',
            subtitle: 'SIC 3674 — NVDA vs. peers (revenue ≥ 10% of NVDA)',
            metric:   'Gross Margin (%)',
            subject:  'NVDA',
            companies: [
              { ticker: 'INTC', name: 'Intel Corp.',         value: 34.8, estimate: false },
              { ticker: 'MU',   name: 'Micron Technology',   value: 39.8, estimate: false },
              { ticker: 'AMAT', name: 'Applied Materials',   value: 48.7, estimate: false },
              { ticker: 'AMD',  name: 'Advanced Micro Devices', value: 49.5, estimate: false },
              { ticker: 'AVGO', name: 'Broadcom Inc.',        value: 67.8, estimate: false },
              { ticker: 'NVDA', name: 'NVIDIA Corp.',         value: 71.1, estimate: false },
            ],
            source:    'SEC EDGAR XBRL frames API, SIC 3674. Corrected even-count median.',
            sparkLine: 'NVDA ranks #1 of 6. Median 49.1%. +22.0pp above sector.',
          })}
        />
      </Folder>
      {/* ── fashionista modifier — photo-critique beat components ── */}
      <Folder name="Fashionista">
        <Composition
          id="LookPlate"
          component={LookPlate}
          durationInFrames={600}
          fps={30}
          width={1920}
          height={1080}
          schema={lookPlateSchema}
          defaultProps={lookPlateSchema.parse({
            imagePath: 'fashionista/2026-08-03/B03.png',
            lookName: 'The Front',
            lookNumber: 3,
            dateFolder: '2026-08-03',
            generatedModel: 'Higgsfield Soul ID',
            lens: 'silhouette',
            rendered: ['Clean vertical center seam, even hem'],
            reference: ['Sherwani — South Asian formal wear, Mughal-era origins'],
            call: 'The silhouette reads intentional front-to-back.',
            notDeterminable: ['fibre content', 'construction quality', 'how this hangs on Bear\'s actual proportions'],
            sparkLine: '',
          })}
        />
        <Composition
          id="LookPlate916"
          component={LookPlate916}
          durationInFrames={600}
          fps={30}
          width={1080}
          height={1920}
          schema={lookPlate916Schema}
          defaultProps={lookPlate916Schema.parse({
            imagePath: 'fashionista/2026-08-03/B03.png',
            lookName: 'The Front',
            lookNumber: 3,
            dateFolder: '2026-08-03',
            generatedModel: 'Higgsfield Soul ID',
            lens: 'silhouette',
            rendered: ['Clean vertical center seam, even hem'],
            reference: ['Sherwani — South Asian formal wear, Mughal-era origins'],
            call: 'The silhouette reads intentional front-to-back.',
            notDeterminable: ['fibre content', 'construction quality', 'how this hangs on Bear\'s actual proportions'],
            sparkLine: '',
          })}
        />
        <Composition
          id="ContactSheet"
          component={ContactSheet}
          durationInFrames={480}
          fps={30}
          width={1920}
          height={1080}
          schema={contactSheetSchema}
          defaultProps={{
            dateFolder: '2026-08-03',
            lens: 'silhouette',
            looks: [
              { name: 'The Front',   imagePath: 'fashionista/2026-08-03/B03.png' },
              { name: 'The Profile', imagePath: 'fashionista/2026-08-03/B04.png' },
              { name: 'The Back',    imagePath: 'fashionista/2026-08-03/B05.png' },
              { name: 'The Hem',     imagePath: 'fashionista/2026-08-03/B07.png' },
            ],
            sparkLine: 'One garment. Five views.',
          }}
        />
        <Composition
          id="ContactSheet916"
          component={ContactSheet916}
          durationInFrames={480}
          fps={30}
          width={1080}
          height={1920}
          schema={contactSheet916Schema}
          defaultProps={{
            dateFolder: '2026-08-03',
            lens: 'silhouette',
            looks: [
              { name: 'The Front',   imagePath: 'fashionista/2026-08-03/B03.png' },
              { name: 'The Profile', imagePath: 'fashionista/2026-08-03/B04.png' },
              { name: 'The Back',    imagePath: 'fashionista/2026-08-03/B05.png' },
              { name: 'The Hem',     imagePath: 'fashionista/2026-08-03/B07.png' },
            ],
            sparkLine: 'One garment. Five views.',
          }}
        />
      </Folder>
      <Folder name="GitHub-Scenes">
        <Composition id="GitHubRepoHero" component={GitHubRepoHero}
          durationInFrames={240} fps={30} width={1920} height={1080}
          schema={gitHubRepoHeroSchema} defaultProps={gitHubRepoHeroSchema.parse({})} />
        <Composition id="GitHubCodeViewer" component={GitHubCodeViewer}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={gitHubCodeViewerSchema} defaultProps={gitHubCodeViewerSchema.parse({})} />
        <Composition id="GitHubCodeDiff" component={GitHubCodeDiff}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={gitHubCodeDiffSchema} defaultProps={gitHubCodeDiffSchema.parse({})} />
        <Composition id="GitHubCallChain" component={GitHubCallChain}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={gitHubCallChainSchema} defaultProps={gitHubCallChainSchema.parse({})} />
        <Composition id="GitHubChurn" component={GitHubChurn}
          durationInFrames={300} fps={30} width={1920} height={1080}
          schema={gitHubChurnSchema} defaultProps={gitHubChurnSchema.parse({})} />
      </Folder>
      <Composition
        id="badge-reveal"
        component={BadgeReveal}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          letter: 'M',
          fontFamily: '"EB Garamond", Georgia, serif',
          badgeColors: ['#F7A8C4', '#E8639B', '#C0417E'],
          gradientAngle: 135,
          markColor: '#FFFFFF',
          ground: '#F6F1F3',
          wordmark: '',
          badgeScale: 0.5,
        }}
      />
    </>
  );
};
