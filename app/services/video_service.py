"""
视频处理服务
处理视频下载、字幕提取、笔记生成
"""
import os
import threading
from flask import current_app
from app.utils.audio import download_audio, download_video
from app.utils.caption import generate_caption
from app.utils.ai import generate_notes_from_text
from app.utils.pdf import create_pdf_from_notes
from app.services.note_service import NoteService


class VideoService:
    """视频处理服务类"""
    
    @staticmethod
    def _download_video_background(app, video_url, video_id):
        """
        后台下载视频（用于影子跟读）
        在独立线程中运行，不阻塞主流程
        
        注意：视频下载失败不影响字幕生成，音频文件仍可用于影子跟读
        """
        import time
        with app.app_context():
            try:
                print(f"\n[Background-{video_id}] ==========================================")
                print(f"[Background-{video_id}] Starting background video download")
                print(f"[Background-{video_id}] URL: {video_url}")
                print(f"[Background-{video_id}] ==========================================")
                
                start_time = time.time()
                video_path = download_video(video_url, download_type='video')
                elapsed = time.time() - start_time
                
                if video_path:
                    print(f"\n[Background-{video_id}] ✓ SUCCESS")
                    print(f"[Background-{video_id}] Video downloaded in {elapsed:.1f}s")
                    print(f"[Background-{video_id}] Path: {video_path}")
                    print(f"[Background-{video_id}] You can now use this video for shadowing practice")
                else:
                    print(f"\n[Background-{video_id}] ✗ FAILED")
                    print(f"[Background-{video_id}] Video download did not complete successfully")
                    print(f"[Background-{video_id}] Don't worry - audio file is still available for shadowing")
                    print(f"[Background-{video_id}] You can practice with audio-only mode")
                    
            except Exception as e:
                print(f"\n[Background-{video_id}] ✗ ERROR in background download")
                print(f"[Background-{video_id}] Error: {e}")
                print(f"[Background-{video_id}] This doesn't affect your subtitle generation")
                print(f"[Background-{video_id}] Audio file is still available for shadowing practice")
                import traceback
                traceback.print_exc()
            finally:
                print(f"[Background-{video_id}] Background thread completed\n")
    
    @staticmethod
    def process_video(video_url, output_format='pdf', save_to_storage=False, download_type='audio'):
        """
        处理视频，生成字幕和笔记
        
        策略：
        1. 总是先下载音频（快速）
        2. 如果用户选择了视频或未指定，后台异步下载视频（用于影子跟读）
        
        Args:
            video_url: 视频URL
            output_format: 输出格式 ('txt' 或 'pdf')
            save_to_storage: 是否保存到笔记存储区
            download_type: 下载类型 ('audio' 或 'video')，默认'audio'会后台下载视频
        
        Returns:
            dict: 处理结果
        """
        result = {'status': 'success'}
        
        # 1. 总是先下载音频（用于快速生成字幕）
        print("=" * 60)
        print("STEP 1/5: Downloading audio...")
        print("=" * 60)
        audio_path = download_audio(video_url)
        
        if not audio_path:
            return {'status': 'error', 'message': '无法下载或处理该视频链接'}
        
        result['audio_path'] = audio_path
        print(f"[OK] Audio saved: {os.path.basename(audio_path)}")
        
        # 2. 提取video_id用于后台下载视频
        video_id = os.path.splitext(os.path.basename(audio_path))[0]
        
        # 3. 启动后台下载任务（总是下载视频用于影子跟读）
        print("\n" + "=" * 60)
        print("STEP 2/5: Starting background video download...")
        print("=" * 60)
        try:
            thread = threading.Thread(
                target=VideoService._download_video_background,
                args=(current_app._get_current_object(), video_url, video_id),
                daemon=True,
                name=f"VideoDownload-{video_id}"
            )
            thread.start()
            result['video_downloading'] = True
            print(f"[OK] Background thread started")
            print(f"  → Video download running in background (won't block subtitle generation)")
            print(f"  → Check console logs for progress")
            print(f"  → If video download fails, audio is still available for shadowing")
        except Exception as e:
            print(f"[WARNING] Failed to start background download: {e}")
            print(f"  → Continuing with audio-only mode")
            result['video_downloading'] = False
        
        # 4. 生成字幕文本（Whisper可以处理视频和音频）
        print("\n" + "=" * 60)
        print("STEP 3/5: Generating subtitles with Whisper...")
        print("=" * 60)
        caption_path, caption_text = generate_caption(audio_path)
        if not caption_path:
            return {'status': 'error', 'message': '生成字幕失败'}
        result['caption_path'] = caption_path
        result['caption_text'] = caption_text
        print(f"[OK] Subtitles saved: {os.path.basename(caption_path)}")
        
        # 3. 根据输出格式处理
        if output_format == 'txt':
            result['filename'] = os.path.basename(caption_path)
            return result
        
        # 4. 生成PDF笔记
        print("\n" + "=" * 60)
        print("STEP 4/5: Generating notes with AI...")
        print("=" * 60)
        notes_text = generate_notes_from_text(caption_text)
        if not notes_text:
            return {'status': 'error', 'message': '调用大模型生成笔记失败'}
        print(f"[OK] Notes generated ({len(notes_text)} characters)")
        
        # 5. 保存MD格式笔记到存储区
        if save_to_storage:
            base_filename = os.path.splitext(os.path.basename(caption_path))[0]
            md_filename = f"{base_filename}_notes.md"
            video_title = f"视频笔记_{base_filename[:20]}"
            NoteService.save_note(md_filename, notes_text, video_title, 'video')
        
        # 6. 创建PDF文件
        print("\n" + "=" * 60)
        print("STEP 5/5: Creating PDF...")
        print("=" * 60)
        base_filename = os.path.splitext(os.path.basename(caption_path))[0]
        pdf_filename = f"{base_filename}_notes.pdf"
        pdf_dir = current_app.config['PDF_DIR']
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        created_pdf_path = create_pdf_from_notes(notes_text, pdf_path)
        if not created_pdf_path:
            return {'status': 'error', 'message': '创建 PDF 文件失败'}
        
        result['pdf_path'] = created_pdf_path
        result['filename'] = pdf_filename
        print(f"[OK] PDF created: {pdf_filename}")
        
        print("\n" + "=" * 60)
        print("[OK] ALL STEPS COMPLETE")
        print("=" * 60)
        print(f"Audio: {os.path.basename(audio_path)}")
        print(f"Video: downloading in background (check logs above)")
        print(f"Subtitles: {os.path.basename(caption_path)}")
        print(f"PDF: {pdf_filename}")
        print(f"\nYou can now use the media in the 'Shadowing' tab")
        print("=" * 60)
        
        return result
