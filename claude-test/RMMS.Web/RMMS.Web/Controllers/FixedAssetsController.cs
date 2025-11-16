using Microsoft.AspNetCore.Mvc;
using RMMS.Models;
using RMMS.Services;

namespace RMMS.Web.Controllers
{
    public class FixedAssetsController : Controller
    {
        private readonly IFixedAssetService _fixedAssetService;
        private readonly ILogger<FixedAssetsController> _logger;

        public FixedAssetsController(IFixedAssetService fixedAssetService, ILogger<FixedAssetsController> logger)
        {
            _fixedAssetService = fixedAssetService;
            _logger = logger;
        }

        public IActionResult Index()
        {
            try
            {
                var assets = _fixedAssetService.GetAll();
                return View(assets);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading fixed assets");
                return View(new List<FixedAsset>());
            }
        }

        public IActionResult Create()
        {
            var model = new FixedAsset
            {
                PurchaseDate = DateTime.Today,
                Status = "Active"
            };
            return View(model);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(FixedAsset model)
        {
            ModelState.Remove("CreatedDate");
            ModelState.Remove("IsActive");

            if (ModelState.IsValid)
            {
                try
                {
                    string currentUsername = User.Identity?.Name ?? "System";
                    _fixedAssetService.Create(model, currentUsername);
                    TempData["Success"] = "Fixed asset created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error creating fixed asset");
                    ModelState.AddModelError("", "Error: " + ex.Message);
                }
            }
            return View(model);
        }

        public IActionResult Edit(int id)
        {
            try
            {
                var asset = _fixedAssetService.GetById(id);
                if (asset == null)
                {
                    return NotFound();
                }
                return View(asset);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading fixed asset for edit");
                TempData["Error"] = "Error loading asset: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, FixedAsset model)
        {
            if (id != model.Id)
            {
                return NotFound();
            }

            if (ModelState.IsValid)
            {
                try
                {
                    string currentUsername = User.Identity?.Name ?? "System";
                    _fixedAssetService.Update(model, currentUsername);
                    TempData["Success"] = "Fixed asset updated successfully!";
                    return RedirectToAction(nameof(Index));
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error updating fixed asset");
                    ModelState.AddModelError("", "An error occurred while updating the asset.");
                }
            }
            return View(model);
        }

        public IActionResult Details(int id)
        {
            try
            {
                var asset = _fixedAssetService.GetById(id);
                if (asset == null)
                {
                    return NotFound();
                }
                return View(asset);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading fixed asset details");
                TempData["Error"] = "Error loading asset details: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Delete(int id)
        {
            try
            {
                string currentUsername = User.Identity?.Name ?? "System";
                _fixedAssetService.Delete(id, currentUsername);
                TempData["Success"] = "Fixed asset deleted successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting fixed asset");
                TempData["Error"] = "Error deleting asset: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        public IActionResult CalculateDepreciation()
        {
            try
            {
                var assets = _fixedAssetService.GetActiveAssets();
                return View(assets);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading assets for depreciation calculation");
                TempData["Error"] = "Error loading assets: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult CalculateDepreciation(int id)
        {
            try
            {
                _fixedAssetService.CalculateDepreciation(id);
                TempData["Success"] = "Depreciation calculated successfully!";
                return RedirectToAction(nameof(CalculateDepreciation));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error calculating depreciation for asset ID {id}");
                TempData["Error"] = "Error calculating depreciation: " + ex.Message;
                return RedirectToAction(nameof(CalculateDepreciation));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult CalculateAllDepreciation()
        {
            try
            {
                var assets = _fixedAssetService.GetActiveAssets();
                int count = 0;
                foreach (var asset in assets)
                {
                    if (asset.DepreciationRate > 0)
                    {
                        _fixedAssetService.CalculateDepreciation(asset.Id);
                        count++;
                    }
                }
                TempData["Success"] = $"Depreciation calculated for {count} asset(s) successfully!";
                return RedirectToAction(nameof(CalculateDepreciation));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error calculating depreciation for all assets");
                TempData["Error"] = "Error calculating depreciation: " + ex.Message;
                return RedirectToAction(nameof(CalculateDepreciation));
            }
        }
    }
}
